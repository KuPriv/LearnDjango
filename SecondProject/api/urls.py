from django.urls import path, include

from rest_framework.routers import DefaultRouter

from .views import APIRubricViewSet


router = DefaultRouter()
router.register("rubrics", APIRubricViewSet)

app_name = "api"
urlpatterns = [
    path("", include(router.urls)),
]
