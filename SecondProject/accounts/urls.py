from django.urls import path, reverse_lazy
from django.contrib.auth.views import (
    LoginView,
    LogoutView,
    PasswordChangeView,
    PasswordChangeDoneView,
)
from .views import *

app_name = "accounts"
urlpatterns = [
    path("login/", LoginView.as_view(), name="login"),
    path("logout/", LogoutView.as_view(next_page="app:index"), name="logout"),
    path(
        "password_change/",
        PasswordChangeView.as_view(
            form_class=MyPasswordChangeForm,
            template_name="registration/change_password.html",
            success_url=reverse_lazy("accounts:password_change_done"),
        ),
        name="password_change",
    ),
    path(
        "password_change/done/",
        PasswordChangeDoneView.as_view(
            template_name="registration/password_changed.html"
        ),
        name="password_change_done",
    ),
]
