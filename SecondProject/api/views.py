from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view, authentication_classes
from rest_framework.response import Response
from rest_framework import status

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
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(["GET", "PUT", "PATCH", "DELETE"])
def api_rubric_detail(request, pk):
    rubric = get_object_or_404(Rubric, pk=pk)
    if request.method == "GET":
        serializer = RubricSerializer(rubric)
        return Response(serializer.data)
    elif request.method == "PUT" or request.method == "PATCH":
        serializer = RubricSerializer(rubric, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    elif request.method == "DELETE":
        rubric.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
