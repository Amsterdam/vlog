import logging

from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIRequestFactory, APITestCase

from vlog.models import Vlog


class TestLineTestCase(APITestCase):
    def test_create_vlogs(self):
        """
        Ensure we can create new objects
        """
        url = reverse('api:vlog-list', kwargs={'version': 'v1'})
        data = """
            2020-01-23 00:00:00.399,6,0600A10500
            2020-01-23 00:00:02.220,10,0A0171010063
            2020-01-23 00:00:02.941,10,0A0171010064
            2020-01-23 00:00:03.521,10,0A0281010465
        """
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Vlog.objects.count(), 4)
        self.assertEqual(Vlog.objects.filter()[0].vri_id, 101)
