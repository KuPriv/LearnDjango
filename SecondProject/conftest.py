import pytest
from django.test import Client


@pytest.fixture
def client():
    return Client()


@pytest.fixture
def user(db, django_user_model):
    return django_user_model.objects.create_user(
        email="example@gmail.com", password="1234"
    )
