from django.urls import path

from . import views
from .views import *

app_name = "app"
urlpatterns = [
    path("", views.index, name="index"),
    path("show_r", views.show_rubric, name="show_r"),
    path("show_m", views.show_measurement, name="show_m"),
    path("set_an", views.set_announcement, name="set_an"),
    path("show_b", views.show_board, name="show_b"),
    path("onetoone", views.OneToOne, name="onetoone"),
    path("manytomany", views.ManyToMany, name="manytomany"),
    path("try_bulk_create", views.try_bulk_create, name="try_bulk_create"),
    path("try_bulk_update", views.try_bulk_update, name="try_bulk_update"),
    path("clear_bb_content", views.clear_bb_content, name="clear_bb_content"),
    path("check_full_clean", views.check_full_clean, name="check_full_clean"),
    path("just_print_results", views.just_print_results, name="just_print_results"),
    path("check_functions_2", views.check_functions_2, name="check_functions_2"),
    path("calculate_fields", views.calculate_fields, name="calculate_fields"),
    path(
        "check_other_functions",
        views.check_other_functions,
        name="check_other_functions",
    ),
    path(
        "access_to_related_records",
        views.access_to_related_records,
        name="access_to_related_records",
    ),
    path("write_some_func/", WriteSomeFunctions.as_view(), name="write_some_func"),
    path("rubrics/", RubricListView.as_view(), name="rubric_list"),
    path("rubric/<int:rubric_id>", views.by_rubric, name="by_rubric"),
    path("add/", views.add_bb_and_save, name="add"),
    path("send_file/", views.send_file, name="send_file"),
    path("detail/<int:bb_id>", views.detail, name="detail"),
    path("detail2/<int:rubric_id>", views.detail2, name="detail2"),
    path("check_resolve", views.check_resolve, name="check_resolve"),
    path("add_class/", BbCreateView.as_view()),
    path(
        "templateview_check/<int:rubric_id>",
        BbByRubricView.as_view(),
        name="bb_by_rubric",
    ),
    # re_path - шаблонные выражения, как и re в Python
]
