from django.utils.cache import patch_cache_control

from ..models import Rubric


class RubricsMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        return self.get_response(request)

    def process_template_response(self, request, response):
        response.context_data["rubrics"] = Rubric.objects.all()
        return response


def my_cache_control_middleware(next):

    def core_middleware(request):
        response = next(request)
        patch_cache_control(response, max_age=0, no_cache=True)
        return response

    return core_middleware
