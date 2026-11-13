import json
import mimetypes
import shutil
from urllib.parse import quote

from cryptography.fernet import InvalidToken
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.db import IntegrityError
from django.http import FileResponse, Http404
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_POST, require_safe
from markdown_it import MarkdownIt

from local_pages.forms import PageForm
from local_pages.models import Page
from local_pages.publishing import PublishError, branches, credential_box, snapshot


def hostname(request):
    return request.get_host().split(":")[0].lower()


def page_url(request, slug):
    _, separator, port = request.get_host().partition(":")
    return f"{request.scheme}://{slug}.{settings.BASE_HOST}{separator}{port}/"


def private(response):
    response["Cache-Control"] = "private, no-store"
    return response


@login_required
@require_safe
def home(request, path=""):
    host = hostname(request)
    if host == settings.BASE_HOST:
        if path:
            raise Http404
        pages = [(page.title, page_url(request, page.slug)) for page in Page.objects.order_by("title")]
        return private(render(request, "directory.html", {
            "pages": pages, "page_url": page_url(request, "welcome"),
        }))
    if host == settings.PAGE_HOST:
        if path:
            raise Http404
        return serve_file(request, settings.BASE_DIR / "example", "index.html")

    slug = host.removesuffix(f".{settings.BASE_HOST}")
    page = get_object_or_404(Page, slug=slug)
    root = settings.PUBLISH_ROOT / str(page.snapshot)
    if not path and "/" in page.entry:
        query = request.META.get("QUERY_STRING", "")
        return private(redirect("/" + quote(page.entry) + ("?" + query if query else "")))
    return serve_file(request, root, path or page.entry, render_markdown=not path)


def serve_file(request, root, path, *, render_markdown=False):
    target = (root / path).resolve()
    if not target.is_relative_to(root.resolve()):
        raise Http404
    if target.is_dir():
        if not request.path.endswith("/"):
            return private(redirect(quote(request.path) + "/"))
        target /= "index.html"
    if not target.is_file():
        raise Http404
    if render_markdown and target.suffix.lower() == ".md":
        content = MarkdownIt().disable("html_block").disable("html_inline").render(
            target.read_text(encoding="utf-8", errors="replace")
        )
        return private(render(request, "markdown.html", {"title": target.stem, "content": content}))
    content_type = {
        ".js": "text/javascript",
        ".mjs": "text/javascript",
        ".md": "text/plain; charset=utf-8",
    }.get(target.suffix.lower()) or mimetypes.guess_type(target.name)[0] or "application/octet-stream"
    try:
        file = target.open("rb")
    except FileNotFoundError as exc:
        raise Http404 from exc
    response = FileResponse(file, content_type=content_type)
    response["Content-Security-Policy"] = "worker-src blob:"
    response["X-Content-Type-Options"] = "nosniff"
    return private(response)


def check_operator(request):
    if hostname(request) != settings.BASE_HOST:
        raise Http404
    if not request.user.is_staff:
        raise PermissionDenied


@login_required
def admin_home(request):
    check_operator(request)
    return admin_list(request)


def admin_list(request, error=None):
    pages = [(page, page_url(request, page.slug)) for page in Page.objects.order_by("title")]
    return private(render(request, "admin_pages.html", {"pages": pages, "error": error}))


@login_required
def add_page(request):
    check_operator(request)
    initial = {"folder": ".", "entry": "index.html"}
    form = PageForm(request.POST if request.method == "POST" else None, initial=initial)
    available = []
    error = None
    if form.is_bound:
        action = request.POST.get("action")
        if action == "branches":
            form.fields["title"].required = False
            form.fields["branch"].required = False
            form.fields["folder"].required = False
            form.fields["entry"].required = False
            form.fields["slug"].required = False
            form.full_clean()
            if not any(field in form.errors for field in ("provider", "repository", "username", "token")):
                try:
                    available = branches(*(form.cleaned_data[field] for field in ("repository", "username", "token")))
                    if not available:
                        error = "This repository has no branches."
                except PublishError as exc:
                    error = str(exc)
                form = PageForm(initial={**request.POST.dict(), "token": ""})
        elif action == "publish" and form.is_valid():
            page = form.save(commit=False)
            username, token = (form.cleaned_data[field] for field in ("username", "token"))
            try:
                snapshot(page, username, token)
            except PublishError as exc:
                error = str(exc)
            else:
                if token:
                    page.credential = credential_box().encrypt(json.dumps([username, token]).encode()).decode()
                try:
                    page.save()
                except IntegrityError:
                    shutil.rmtree(settings.PUBLISH_ROOT / str(page.snapshot), ignore_errors=True)
                    form.add_error("slug", "This subdomain is already in use.")
                else:
                    return redirect("admin_home")
    return private(render(request, "add_page.html", {
        "form": form, "branches": available, "error": error, "base_host": settings.BASE_HOST,
    }))


@login_required
@require_POST
def refresh_page(request, slug):
    check_operator(request)
    page = get_object_or_404(Page, slug=slug)
    previous = page.snapshot
    try:
        username, token = json.loads(credential_box().decrypt(page.credential.encode())) if page.credential else ("", "")
        snapshot(page, username, token)
    except InvalidToken:
        return admin_list(request, "The saved Git credential cannot be read. Check the installation secret.")
    except PublishError as exc:
        return admin_list(request, str(exc))
    if Page.objects.filter(pk=page.pk, snapshot=previous).update(snapshot=page.snapshot, revision=page.revision):
        old_snapshot = previous
    else:
        old_snapshot = page.snapshot
    shutil.rmtree(settings.PUBLISH_ROOT / str(old_snapshot), ignore_errors=True)
    return redirect("admin_home")
