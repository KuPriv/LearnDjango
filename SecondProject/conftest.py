import pytest
from django.db import connection
from django.test import Client


@pytest.fixture
def client():
    return Client()


@pytest.fixture
def user(db, django_user_model):
    return django_user_model.objects.create_user(
        email="example@gmail.com", password="1234"
    )


@pytest.fixture(autouse=True)
def ensure_extensions(db):
    with connection.cursor() as cursor:
        cursor.execute("CREATE EXTENSION IF NOT EXISTS hstore;")
        cursor.execute("CREATE EXTENSION IF NOT EXISTS btree_gist;")
        cursor.execute("CREATE EXTENSION IF NOT EXISTS pg_trgm;")
