from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.http import FileResponse
from django.shortcuts import render


@login_required
def home(request):
    if request.get_host().split(":")[0] == settings.PAGE_HOST:
        response = FileResponse(
            (settings.BASE_DIR / "example" / "index.html").open("rb"),
            content_type="text/html; charset=utf-8",
        )
    else:
        response = directory(request)
    response["Cache-Control"] = "private, no-store"
    return response


def directory(request):
    _, separator, port = request.get_host().partition(":")
    url = f"{request.scheme}://{settings.PAGE_HOST}{separator}{port}/"
    return render(request, "directory.html", {"page_url": url})
