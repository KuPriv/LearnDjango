from django.contrib import admin
from .models import *

admin.site.register(Rubric)
admin.site.register(Bb)
admin.site.register(AdvUser)
admin.site.register(Board)
admin.site.register(Measure)
admin.site.register(Machine)


@admin.register(Spare)
class SpareAdmin(admin.ModelAdmin):
    list_display = ("name",)
    actions = ["delete_selected"]
