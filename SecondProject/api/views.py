from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view, authentication_classes
from rest_framework.response import Response

from .authentication import CsrfExemptSessionAuthentication
from .serializers import RubricSerializer
from app.models import Rubric


@api_view(["GET", "POST"])
@authentication_classes([CsrfExemptSessionAuthentication])
def api_rubrics(request):
    if request.method == "GET":
        rubrics = Rubric.objects.all()
        serializer = RubricSerializer(rubrics, many=True)
        return Response(serializer.data)
    elif request.method == "POST":
        serializer = RubricSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)


@api_view(["GET"])
def api_rubric_detail(request, pk):
    if request.method == "GET":
        rubric = get_object_or_404(Rubric, pk=pk)
        serializer = RubricSerializer(rubric)
        return Response(serializer.data)
