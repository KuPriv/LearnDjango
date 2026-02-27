from django.urls import path
from .views import api_rubrics, api_rubric_detail, APIRubrics, APIRubricDetail

app_name = "api"
urlpatterns = [
    path("rubrics/<int:pk>/", APIRubricDetail.as_view(), name="rubric_detail"),
    path("rubrics/", APIRubrics.as_view(), name="api_rubrics"),
]
