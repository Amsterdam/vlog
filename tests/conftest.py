import pytest
from pytest_factoryboy import register
from rest_framework.authtoken.models import Token
from rest_framework.test import APIClient

from .factories import UserFactory

register(UserFactory)


@pytest.fixture
def api_client():
    return APIClient()


@pytest.fixture
def authd_api_client(api_client, user):
    api_client.force_authenticate(user=user)
    return api_client


@pytest.fixture
def token_api_client(api_client, user):
    token, created = Token.objects.get_or_create(user=user)
    api_client.credentials(HTTP_AUTHORIZATION=f"Token {token.key}")
    return api_client
