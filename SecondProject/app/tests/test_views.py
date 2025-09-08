from django.urls import reverse
from django.urls import get_resolver


def test_show_url_patterns():
    print([r.pattern for r in get_resolver().url_patterns])
