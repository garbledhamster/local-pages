import os
from pathlib import Path

from django.core.management.utils import get_random_secret_key

BASE_DIR = Path(__file__).resolve().parent.parent
BASE_HOST = os.environ.get("LOCAL_PAGES_HOST", "pages.localhost")
PAGE_HOST = f"welcome.{BASE_HOST}"
SECRET_KEY = os.environ.get("LOCAL_PAGES_SECRET_KEY") or get_random_secret_key()
ALLOWED_HOSTS = [f".{BASE_HOST}"]
PUBLISH_ROOT = Path(os.environ.get("LOCAL_PAGES_PUBLISH_ROOT", BASE_DIR / "data" / "sites"))
ALLOW_FILE_REPOSITORIES = False
INSECURE_GIT_HOSTS = os.environ.get("LOCAL_PAGES_INSECURE_GIT_HOSTS", "").split()
if os.environ.get("LOCAL_PAGES_HTTPS") == "1":
    SESSION_COOKIE_NAME = "__Host-localpages"
    SESSION_COOKIE_SECURE = True
    CSRF_COOKIE_NAME = "__Host-localpages-csrf"
    CSRF_COOKIE_SECURE = True
    SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")
ROOT_URLCONF = "local_pages.urls"
WSGI_APPLICATION = "local_pages.wsgi.application"
INSTALLED_APPS = [
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "local_pages",
]
MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]
TEMPLATES = [{
    "BACKEND": "django.template.backends.django.DjangoTemplates",
    "DIRS": [BASE_DIR / "templates"],
    "APP_DIRS": True,
    "OPTIONS": {"context_processors": ["django.template.context_processors.request"]},
}]
DATABASES = {"default": {
    "ENGINE": "django.db.backends.sqlite3",
    "NAME": os.environ.get("LOCAL_PAGES_DATABASE", BASE_DIR / "db.sqlite3"),
}}
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"
LOGIN_REDIRECT_URL = "/"
LOGOUT_REDIRECT_URL = "/accounts/login/"
