from django.core.exceptions import ValidationError


class NoForbiddenCharsValidator:
    FORBIDDEN = set("!@#$%")

    def validate(self, password, user=None):
        if any(char in self.FORBIDDEN for char in password):
            raise ValidationError(self.get_help_text())

    def get_help_text(self):
        return "Password must not contain forbidden characters."
