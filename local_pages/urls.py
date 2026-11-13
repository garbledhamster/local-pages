from django.contrib.auth.views import LoginView, LogoutView
from django.urls import path

from local_pages.views import home

urlpatterns = [
    path("", home, name="directory"),
    path("accounts/login/", LoginView.as_view(), name="login"),
    path("accounts/logout/", LogoutView.as_view(), name="logout"),
]
