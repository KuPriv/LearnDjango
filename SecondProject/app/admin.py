from django.contrib import admin
from .models import *

admin.site.register(AdvUser)
admin.site.register(Measure)
admin.site.register(SuperRubric)
admin.site.register(Message)
admin.site.register(PrivateMessage)


@admin.register(Spare)
class SpareAdmin(admin.ModelAdmin):
    list_display = ("name",)
    actions = ["delete_selected"]


@admin.register(Rubric)
class RubricAdmin(admin.ModelAdmin):
    list_display = ("name", "pk")
    actions = ["delete_selected"]


@admin.register(Magazine)
class MagazineAdmin(admin.ModelAdmin):
    list_display = ("title",)
    actions = ["delete_selected"]


@admin.register(Board)
class BoardAdmin(admin.ModelAdmin):
    list_display = ("title",)
    actions = ["delete_selected"]


@admin.register(Bb)
class BbAdmin(admin.ModelAdmin):
    list_display = (
        "title",
        "price",
        "created_at",
        "updated_at",
        "pk",
    )
    actions = ["delete_selected"]


class KitInline(admin.TabularInline):
    model = Kit
    extra = 0


@admin.register(Machine)
class MachineAdmin(admin.ModelAdmin):
    inlines = [KitInline]


@admin.register(Kit)
class KitAdmin(admin.ModelAdmin):
    list_display = ("machine", "spare", "count", "pk")
    actions = ["delete_selected"]


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ("user", "bb", "comment")
    actions = ["delete_selected"]
