import pytest
from pytest_factoryboy import register

from .factories import VlogFactory

register(VlogFactory)


@pytest.fixture
def api_client():
    from rest_framework.test import APIClient
    return APIClient()
