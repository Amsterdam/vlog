import pytest
from django.conf import settings
from pytest_factoryboy import register
from rest_framework.authtoken.models import Token
from rest_framework.test import APIClient


@pytest.fixture
def api_client():
    return APIClient()


@pytest.fixture
def authd_api_client(api_client):
    api_client.credentials(HTTP_AUTHORIZATION=f"Token {settings.AUTHORIZATION_TOKEN}")
    return api_client
