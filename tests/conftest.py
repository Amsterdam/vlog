import pytest
from django.conf import settings
from rest_framework.test import APIClient


@pytest.fixture
def api_client():
    return APIClient()


@pytest.fixture
def authd_api_client(api_client):
    api_client.credentials(HTTP_AUTHORIZATION=f"Token {settings.AUTHORIZATION_TOKEN}")
    return api_client
