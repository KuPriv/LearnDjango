from django.contrib.auth.models import User
from django.core.validators import EmailValidator
from django.db import models


class AdvUser(models.Model):
    is_activated = models.BooleanField(default=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    email = models.EmailField(
        blank=True, validators=[EmailValidator(message="Invalid email")]
    )
