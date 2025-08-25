from django.urls import path, reverse_lazy
from django.contrib.auth.views import LoginView, LogoutView, PasswordChangeView
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
            success_url=reverse_lazy("app:index"),
        ),
        name="password_change",
    ),
]
