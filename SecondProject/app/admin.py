from django.contrib import admin
from .models import *

admin.site.register(Measure)
admin.site.register(SuperRubric)
admin.site.register(Message)
admin.site.register(PrivateMessage)
admin.site.empty_value_display = "(пусто)"


class PriceListFilter(admin.SimpleListFilter):
    title = "Категория цен"
    parameter_name = "price"

    def lookups(self, request, model_admin):
        return (
            ("low", "Низкая цена"),
            ("medium", "Средняя цена"),
            ("high", "Высокая цена"),
        )

    def queryset(self, request, queryset):
        if self.value() == "low":
            return queryset.filter(price__lt=500)
        elif self.value() == "medium":
            return queryset.filter(price__gte=500, price__lte=5000)
        elif self.value() == "high":
            return queryset.filter(price__gt=5000)


@admin.register(Spare)
class SpareAdmin(admin.ModelAdmin):
    list_display = ("name",)
    actions = ["delete_selected"]


@admin.register(Rubric)
class RubricAdmin(admin.ModelAdmin):
    list_display = ("name", "pk", "super_rubric")
    fields = ("name", "super_rubric")

    def super_rubric(self, rec):
        return rec.super_rubric.name

    super_rubric.empty_value_display = "[нет]"

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        else:
            return qs.filter(is_hidden=False)

    actions = ["delete_selected"]


@admin.register(Magazine)
class MagazineAdmin(admin.ModelAdmin):
    list_display = ("title", "rubric")
    list_display_links = ("title",)
    list_editable = ("rubric",)

    def get_list_display(self, request):
        ld = ("title", "price", "rubric")
        if request.user.is_superuser:
            ld += ("published",)
        return ld

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
    list_filter = (PriceListFilter,)
    search_fields = ("title", "content")
    date_hierarchy = "created_at"

    empty_value_display = "---"
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


@admin.register(PGSRoomReserving)
class PGSRoomReservingAdmin(admin.ModelAdmin):
    list_display = ("name", "reserving", "cancelled")
    actions = ["delete_selected"]


@admin.register(PGSRubric)
class PGSRubricAdmin(admin.ModelAdmin):
    list_display = ("name", "description", "tags", "pk")
    actions = ["delete_selected"]


@admin.register(Img)
class ImgAdmin(admin.ModelAdmin):
    list_display = ("img", "pk", "desc")
    actions = ["delete_selected"]
