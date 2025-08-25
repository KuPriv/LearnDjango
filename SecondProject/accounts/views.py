from django.contrib.auth import get_user_model
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.password_validation import (
    get_default_password_validators,
    validate_password,
)
from django.core.exceptions import ValidationError
from django.shortcuts import render


class MyPasswordChangeForm(PasswordChangeForm):

    def clean(self):
        cleaned_data = super().clean()

        for fld in ("new_password1", "new_password2"):
            if getattr(self, "_errors", None) and fld in self._errors:
                del self._errors[fld]

        pwd1 = cleaned_data.get("password1")
        pwd2 = cleaned_data.get("password2")

        if pwd1 and pwd2:
            if pwd1 != pwd2:
                self.add_error("new_password2", "Пароли не совпадают")
            else:
                pass

        return cleaned_data
