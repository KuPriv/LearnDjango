from django.urls import path
from .views import api_rubrics, api_rubric_detail

app_name = "api"
urlpatterns = [
    path("rubric_detail/<int:pk>/", api_rubric_detail, name="rubric_detail"),
    path("rubrics/", api_rubrics, name="api_rubrics"),
]
