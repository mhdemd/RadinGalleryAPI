import pytest
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient

from categories.models import Category

User = get_user_model()


@pytest.fixture
def user(db):
    return User.objects.create_user(
        email="user@example.com", password="testpassword", is_active=True
    )