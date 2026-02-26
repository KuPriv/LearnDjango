from rest_framework.decorators import api_view
from rest_framework.response import Response


from .serializers import RubricSerializer
from app.models import Rubric


@api_view(["GET"])
def api_rubrics(request):
    if request.method == "GET":
        rubrics = Rubric.objects.all()
        serializer = RubricSerializer(rubrics, many=True)
        return Response(serializer.data)
