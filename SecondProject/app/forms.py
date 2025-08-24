from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.forms import ModelForm, DecimalField, Select
from django import forms
from .models import Bb, Rubric


class BbForm(ModelForm):
    class Meta:
        model = Bb
        fields = ("title", "content", "price", "rubric")
        labels = {"title": "Nazvanie TOVARA"}
        help_texts = ({"rubric": "Не забудь выбрать рубрику"},)
        field_classes = ({"price": DecimalField},)
        widgets = ({"rubric": Select(attrs={"size": 8})},)
        error_messages = {
            "title": {
                "required": "Типа поля надо заполнить все",
            },
        }


class BbForm(forms.ModelForm):
    price = forms.DecimalField(label="Цена", decimal_places=2)
    rubric = forms.ModelChoiceField(
        queryset=Rubric.objects.all(),
        label="Рубрика",
        help_text="Задай рубрику",
        widget=forms.widgets.Select(attrs={"size": 8}),
    )
    calendar_field = forms.DateField(
        label="Дата", widget=forms.SelectDateWidget(years=(2000 + i for i in range(30)))
    )
    # text = forms.CharField(widget=forms.Textarea)
    checkbox = forms.BooleanField(
        label="Соглашайся, падла",
        widget=forms.CheckboxInput,
    )

    def clean(self):
        super().clean()
        errors = {}
        if not self.cleaned_data["content"]:
            errors.content = ValidationError("Описания нет.")
        if self.cleaned_data["price"] < 0:
            errors.price = ValidationError("Цена не может быть меньше 0")

        if errors:
            raise ValidationError(errors)

    class Meta:
        model = Bb
        fields = ("title", "content", "price", "rubric")
        labels = {"title": "Название товара"}


class RegisterUserForm(forms.ModelForm):
    password1 = forms.CharField(label="Пароль", widget=forms.widgets.PasswordInput)
    password2 = forms.CharField(
        label="Пароль (повторно)", widget=forms.widgets.PasswordInput
    )

    class Meta:
        model = User
        fields = (
            "username",
            "email",
            "password1",
            "password2",
            "first_name",
            "last_name",
        )

    def clean(self):
        cleaned_data = super().clean()
        p1 = cleaned_data.get("password1")
        p2 = cleaned_data.get("password2")
        if p1 and p2 and p1 != p2:
            raise forms.ValidationError()
        else:
            return cleaned_data

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user
