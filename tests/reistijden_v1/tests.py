from django.conf import settings
from rest_framework.test import APITestCase

from src.reistijden_v1.models import (IndividualTravelTime, Location, Measurement, Publication,
                                      TrafficFlow, TravelTime)
from .test_xml import (TEST_POST_INDIVIDUAL_TRAVEL_TIME,
                       TEST_POST_TRAFFIC_FLOW, TEST_POST_TRAVEL_TIME)

AUTHORIZATION_HEADER = {'HTTP_AUTHORIZATION': f"Token {settings.AUTHORIZATION_TOKEN}"}


class ReistijdenPostTest(APITestCase):
    def setUp(self):
        self.URL = '/reistijden/v1/'

    def test_post_new_travel_time(self):
        """ Test posting a new vanilla travel time message """
        response = self.client.post(self.URL, TEST_POST_TRAVEL_TIME, **AUTHORIZATION_HEADER, format='xml')

        self.assertEqual(response.status_code, 201, response.data)
        self.assertEqual(Publication.objects.all().count(), 1)
        self.assertEqual(Measurement.objects.all().count(), 2)
        self.assertEqual(Location.objects.all().count(), 6)
        self.assertEqual(TravelTime.objects.all().count(), 2)
        self.assertEqual(IndividualTravelTime.objects.all().count(), 0)
        self.assertEqual(TrafficFlow.objects.all().count(), 0)

    def test_post_new_individual_travel_time(self):
        """ Test posting a new vanilla travel time message """
        response = self.client.post(self.URL, TEST_POST_INDIVIDUAL_TRAVEL_TIME, **AUTHORIZATION_HEADER, format='xml')

        self.assertEqual(response.status_code, 201, response.data)
        self.assertEqual(Publication.objects.all().count(), 1)
        self.assertEqual(Measurement.objects.all().count(), 2)
        self.assertEqual(Location.objects.all().count(), 4)
        self.assertEqual(TravelTime.objects.all().count(), 0)
        self.assertEqual(IndividualTravelTime.objects.all().count(), 5)
        self.assertEqual(TrafficFlow.objects.all().count(), 0)

    def test_post_new_traffic_flow(self):
        """ Test posting a new vanilla travel time message """
        response = self.client.post(self.URL, TEST_POST_TRAFFIC_FLOW, **AUTHORIZATION_HEADER, format='xml')

        self.assertEqual(response.status_code, 201, response.data)
        self.assertEqual(Publication.objects.all().count(), 1)
        self.assertEqual(Measurement.objects.all().count(), 3)
        self.assertEqual(Location.objects.all().count(), 3)
        self.assertEqual(TravelTime.objects.all().count(), 0)
        self.assertEqual(IndividualTravelTime.objects.all().count(), 0)
        self.assertEqual(TrafficFlow.objects.all().count(), 3)

    def test_post_fails_without_token(self):
        response = self.client.post(self.URL, TEST_POST_TRAVEL_TIME, format='xml')
        self.assertEqual(response.status_code, 401)

    def test_post_wrongy_formatted_xml(self):
        response = self.client.post(self.URL, '<wrongly>formatted</xml>', **AUTHORIZATION_HEADER, format='xml')
        self.assertEqual(response.status_code, 400, response.data)

    def test_post_wrongy_formatted_message_structure(self):
        response = self.client.post(self.URL, '<root>wrong structure</root>', **AUTHORIZATION_HEADER, format='xml')
        self.assertEqual(response.status_code, 400, response.data)

    def test_get_method_not_allowed(self):
        """ Test if getting a peoplemeasurement is not allowed """
        # First post one
        response = self.client.post(self.URL, TEST_POST_TRAVEL_TIME, **AUTHORIZATION_HEADER, format='xml')
        self.assertEqual(response.status_code, 201)

        # Then check if I cannot get it
        response = self.client.get(f'{self.URL}1/', **AUTHORIZATION_HEADER)
        self.assertEqual(response.status_code, 405)

    def test_update_method_not_allowed(self):
        """ Test if updating a peoplemeasurement is not allowed """
        # First post one
        response = self.client.post(self.URL, TEST_POST_TRAVEL_TIME, **AUTHORIZATION_HEADER, format='xml')
        self.assertEqual(response.status_code, 201)

        # Then check if I cannot update it
        response = self.client.put(f'{self.URL}1/', TEST_POST_TRAVEL_TIME, **AUTHORIZATION_HEADER, format='xml')
        self.assertEqual(response.status_code, 405)

    def test_delete_method_not_allowed(self):
        """ Test if deleting a peoplemeasurement is not allowed """
        # First post one
        response = self.client.post(self.URL, TEST_POST_TRAVEL_TIME, **AUTHORIZATION_HEADER, format='xml')
        self.assertEqual(response.status_code, 201)

        # Then check if I cannot delete it
        response = self.client.delete(f'{self.URL}1/', **AUTHORIZATION_HEADER)
        self.assertEqual(response.status_code, 405)
