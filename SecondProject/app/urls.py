from django.urls import path

from . import views

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
]
