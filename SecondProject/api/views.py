from django.shortcuts import get_object_or_404
from django.http import Http404

from rest_framework.decorators import api_view, authentication_classes
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from rest_framework import generics
from rest_framework.viewsets import ModelViewSet

from .authentication import CsrfExemptSessionAuthentication
from .serializers import RubricSerializer
from app.models import Rubric


class APIRubricViewSet(ModelViewSet):
    queryset = Rubric.objects.all()
    serializer_class = RubricSerializer
