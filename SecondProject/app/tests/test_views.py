from django.urls import reverse
from django.urls import get_resolver


def test_an_admin_view(admin_client):
    url = reverse("admin:index")
    response = admin_client.get(url, secure=True)
    assert response.status_code == 200
