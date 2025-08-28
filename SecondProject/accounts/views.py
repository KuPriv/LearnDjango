from django.contrib.auth import get_user_model
from django.contrib.auth.forms import PasswordChangeForm, SetPasswordForm
from django.contrib.auth.password_validation import (
    get_default_password_validators,
    validate_password,
)
from django.core.exceptions import ValidationError
from django.shortcuts import render

from .utils.forms import clean_passwords


class MyPasswordChangeForm(PasswordChangeForm):

    def clean(self):
        super().clean()
        return clean_passwords(self, "new_password1", "new_password2")


class MyPasswordSetForm(SetPasswordForm):

    def clean(self):
        super().clean()
        return clean_passwords(self, "new_password1", "new_password2")
