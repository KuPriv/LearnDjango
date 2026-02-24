from django.contrib import admin

from .models import AdvUser


@admin.register(AdvUser)
class AdvUserAdmin(admin.ModelAdmin):
    list_display = ("username", "email", "is_activated", "full_name")

    @admin.display(description="Полное имя", ordering="user__last_name")
    def full_name(self, obj):
        return f"{obj.user.first_name} {obj.user.last_name}"

    def username(self, obj):
        return obj.user.username
