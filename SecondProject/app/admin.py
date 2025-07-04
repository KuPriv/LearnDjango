from django.contrib import admin
from .models import *

admin.site.register(Bb)
admin.site.register(AdvUser)
admin.site.register(Measure)
admin.site.register(Machine)


@admin.register(Spare)
class SpareAdmin(admin.ModelAdmin):
    list_display = ("name",)
    actions = ["delete_selected"]


@admin.register(Rubric)
class RubricAdmin(admin.ModelAdmin):
    list_display = ("name",)
    actions = ["delete_selected"]


@admin.register(Magazine)
class MagazineAdmin(admin.ModelAdmin):
    list_display = ("title",)
    actions = ["delete_selected"]


@admin.register(Board)
class BoardAdmin(admin.ModelAdmin):
    list_display = ("title",)
    actions = ["delete_selected"]
