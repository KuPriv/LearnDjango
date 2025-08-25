from django.contrib.auth import get_user_model
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.password_validation import (
    get_default_password_validators,
    validate_password,
)
from django.shortcuts import render

User = get_user_model()


class MyPasswordChangeForm(PasswordChangeForm):

    def clean_new_password1(self):
        password1 = self.cleaned_data.get("new_password1")
        if password1:
            validators = [
                v
                for v in get_default_password_validators()
                if v.__class__.__name__ != "CommonPasswordValidator"
            ]
            validate_password(password1, self.user, validators)
        return password1
