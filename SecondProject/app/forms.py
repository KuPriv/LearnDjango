from django.forms import ModelForm

from .models import Bb


class BbForm(ModelForm):
    class Meta:
        model = Bb
        fields = ("title", "content", "price", "rubric")
        error_messages = {
            "title": {
                "required": "Типа поля надо заполнить все",
            },
        }
