import re
from pathlib import PurePosixPath

from django import forms
from django.utils.text import slugify

from local_pages.models import Page
from local_pages.publishing import PublishError, relative_path, validate_repository


class PageForm(forms.ModelForm):
    provider = forms.ChoiceField(choices=[("gitea", "Gitea"), ("github", "GitHub"), ("gitlab", "GitLab")])
    repository = forms.CharField(label="Repository URL", max_length=500)
    username = forms.CharField(label="Git username", max_length=150, required=False)
    token = forms.CharField(label="Read-only token", widget=forms.PasswordInput, required=False, max_length=500)
    slug = forms.CharField(label="Subdomain", max_length=63, required=False)

    class Meta:
        model = Page
        fields = ("title", "provider", "repository", "username", "token", "branch", "folder", "entry", "slug")
        labels = {"title": "Page name", "folder": "Publish folder", "entry": "Entry file"}

    def clean_repository(self):
        value = self.cleaned_data["repository"]
        try:
            validate_repository(value)
        except (PublishError, ValueError) as exc:
            raise forms.ValidationError(str(exc)) from exc
        return value

    def clean_slug(self):
        value = self.cleaned_data["slug"] or slugify(self.cleaned_data.get("title", ""))[:63].rstrip("-")
        if not re.fullmatch(r"[a-z0-9](?:[a-z0-9-]{0,61}[a-z0-9])?", value) or value == "welcome":
            raise forms.ValidationError("Use a unique subdomain with letters, numbers, and hyphens.")
        return value

    def clean_folder(self):
        return self.clean_relative("folder")

    def clean_entry(self):
        value = self.clean_relative("entry")
        if PurePosixPath(value).suffix.lower() not in {".html", ".htm", ".md"}:
            raise forms.ValidationError("Choose an HTML or Markdown entry file.")
        return value

    def clean_relative(self, field):
        try:
            return relative_path(self.cleaned_data[field])
        except PublishError as exc:
            raise forms.ValidationError(str(exc)) from exc
