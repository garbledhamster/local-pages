from django.contrib.auth.views import LoginView, LogoutView
from django.urls import path

from local_pages.views import add_page, admin_home, home, refresh_page

urlpatterns = [
    path("", home, name="directory"),
    path("accounts/login/", LoginView.as_view(), name="login"),
    path("accounts/logout/", LogoutView.as_view(), name="logout"),
    path("admin/", admin_home, name="admin_home"),
    path("admin/add/", add_page, name="add_page"),
    path("admin/<slug:slug>/refresh/", refresh_page, name="refresh_page"),
    path("<path:path>", home),
]
