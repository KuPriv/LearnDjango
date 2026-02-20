from .models import Rubric


def rubrics(request):
    return {"rubrics": Rubric.objects.all()}
