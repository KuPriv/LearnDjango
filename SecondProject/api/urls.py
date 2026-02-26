from django.urls import path
from .views import api_rubrics

app_name = "api"
urlpatterns = [
    path("rubrics/", api_rubrics, name="api_rubrics"),
]
