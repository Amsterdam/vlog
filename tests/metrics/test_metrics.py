import pytest
from django.urls import reverse
from rest_framework import status


class TestMetrics:
    def test_metrics_endpoint(self, api_client):
        """
        Ensure the metrics endpoint exists and returns prometheus metrics
        """
        url = reverse('metrics')
        response = api_client.get(url)
        assert response.status_code == status.HTTP_200_OK
        assert b'python_info' in response.content
        assert b'process_start_time_seconds' in response.content
