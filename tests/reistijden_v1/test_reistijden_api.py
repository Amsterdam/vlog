from datetime import datetime

from dateutil import parser
from django.conf import settings
from rest_framework.test import APITestCase

from reistijden_v1.models import (Category, IndividualTravelTime, Lane,
                                  Location, MeasuredFlow, Measurement,
                                  Publication, TravelTime)
from tests.reistijden_v1.test_xml import (
    TEST_POST_EMPTY, TEST_POST_INDIVIDUAL_TRAVEL_TIME,
    TEST_POST_INDIVIDUAL_TRAVEL_TIME_SINGLE_MEASUREMENT,
    TEST_POST_TRAFFIC_FLOW, TEST_POST_TRAVEL_TIME, TEST_POST_WRONG_TAGS)

AUTHORIZATION_HEADER = {'HTTP_AUTHORIZATION': f"Token {settings.AUTHORIZATION_TOKEN}"}
CONTENT_TYPE_HEADER = {'content_type': 'application/xml'}
REQUEST_HEADERS = {**AUTHORIZATION_HEADER, **CONTENT_TYPE_HEADER}


class ReistijdenPostTest(APITestCase):
    def setUp(self):
        self.URL = '/reistijden/v1/'

    def test_post_new_travel_time(self):
        """ Test posting a new vanilla travel time message """
        response = self.client.post(self.URL, TEST_POST_TRAVEL_TIME['source'], **REQUEST_HEADERS)

        self.assertEqual(response.status_code, 201, response.data)
        self.assertEqual(Publication.objects.all().count(), 1)
        self.assertEqual(Measurement.objects.all().count(), 2)
        self.assertEqual(Location.objects.all().count(), 6)
        self.assertEqual(Lane.objects.all().count(), 7)
        self.assertEqual(TravelTime.objects.all().count(), 5)
        self.assertEqual(IndividualTravelTime.objects.all().count(), 0)
        self.assertEqual(MeasuredFlow.objects.all().count(), 0)
        self.assertEqual(Category.objects.all().count(), 0)

        publication = Publication.objects.first()
        for k, v in TEST_POST_TRAVEL_TIME['publication'].items():
            if type(getattr(publication, k)) is datetime:
                self.assertEqual(getattr(publication, k), parser.parse(v))
            else:
                self.assertEqual(getattr(publication, k), v)

    def test_post_new_individual_travel_time(self):
        """ Test posting a new vanilla individual travel time message """
        response = self.client.post(self.URL, TEST_POST_INDIVIDUAL_TRAVEL_TIME, **REQUEST_HEADERS)

        self.assertEqual(response.status_code, 201, response.data)
        self.assertEqual(Publication.objects.all().count(), 1)
        self.assertEqual(Measurement.objects.all().count(), 2)
        self.assertEqual(Location.objects.all().count(), 4)
        self.assertEqual(Lane.objects.all().count(), 4)
        self.assertEqual(TravelTime.objects.all().count(), 0)
        self.assertEqual(IndividualTravelTime.objects.all().count(), 3)
        self.assertEqual(MeasuredFlow.objects.all().count(), 0)
        self.assertEqual(Category.objects.all().count(), 0)

    def test_post_new_individual_travel_time_with_single_measurement(self):
        """ Test posting a new individual travel time message with a single measurement """
        response = self.client.post(self.URL, TEST_POST_INDIVIDUAL_TRAVEL_TIME_SINGLE_MEASUREMENT, **REQUEST_HEADERS)

        self.assertEqual(response.status_code, 201, response.data)
        self.assertEqual(Publication.objects.all().count(), 1)
        self.assertEqual(Measurement.objects.all().count(), 1)
        self.assertEqual(Location.objects.all().count(), 2)
        self.assertEqual(Lane.objects.all().count(), 2)
        self.assertEqual(TravelTime.objects.all().count(), 0)
        self.assertEqual(IndividualTravelTime.objects.all().count(), 2)
        self.assertEqual(MeasuredFlow.objects.all().count(), 0)
        self.assertEqual(Category.objects.all().count(), 0)

    def test_post_new_traffic_flow(self):
        """ Test posting a new vanilla traffic flow message """
        response = self.client.post(self.URL, TEST_POST_TRAFFIC_FLOW, **REQUEST_HEADERS)

        self.assertEqual(response.status_code, 201, response.data)
        self.assertEqual(Publication.objects.all().count(), 1)
        self.assertEqual(Measurement.objects.all().count(), 3)
        self.assertEqual(Location.objects.all().count(), 3)
        self.assertEqual(Lane.objects.all().count(), 3)
        self.assertEqual(TravelTime.objects.all().count(), 0)
        self.assertEqual(IndividualTravelTime.objects.all().count(), 0)
        self.assertEqual(MeasuredFlow.objects.all().count(), 4)
        self.assertEqual(Category.objects.all().count(), 5)

    def test_empty_measurement(self):
        response = self.client.post(self.URL, TEST_POST_EMPTY, **REQUEST_HEADERS)

        self.assertEqual(response.status_code, 201, response.data)
        self.assertEqual(Publication.objects.all().count(), 1)
        self.assertEqual(Measurement.objects.all().count(), 0)
        self.assertEqual(Location.objects.all().count(), 0)
        self.assertEqual(Lane.objects.all().count(), 0)
        self.assertEqual(TravelTime.objects.all().count(), 0)
        self.assertEqual(IndividualTravelTime.objects.all().count(), 0)
        self.assertEqual(MeasuredFlow.objects.all().count(), 0)
        self.assertEqual(Category.objects.all().count(), 0)

    def test_expaterror(self):
        response = self.client.post(self.URL, TEST_POST_WRONG_TAGS, **REQUEST_HEADERS)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.data, 'not well-formed (invalid token): line 11, column 5')
        self.assertEqual(Publication.objects.all().count(), 0)
        self.assertEqual(Measurement.objects.all().count(), 0)
        self.assertEqual(Location.objects.all().count(), 0)
        self.assertEqual(Lane.objects.all().count(), 0)
        self.assertEqual(TravelTime.objects.all().count(), 0)
        self.assertEqual(IndividualTravelTime.objects.all().count(), 0)
        self.assertEqual(MeasuredFlow.objects.all().count(), 0)
        self.assertEqual(Category.objects.all().count(), 0)

    def test_post_fails_without_token(self):
        response = self.client.post(self.URL, TEST_POST_TRAVEL_TIME['source'], **CONTENT_TYPE_HEADER)
        self.assertEqual(response.status_code, 401)

    def test_post_wrongy_formatted_xml(self):
        response = self.client.post(self.URL, '<wrongly>formatted</xml>', **REQUEST_HEADERS)
        self.assertEqual(response.status_code, 400, response.data)

    def test_post_wrongy_formatted_message_structure(self):
        response = self.client.post(self.URL, '<root>wrong structure</root>', **REQUEST_HEADERS)
        self.assertEqual(response.status_code, 400, response.data)

    def test_non_unicode(self):
        response = self.client.post(self.URL, '\x80abc', **REQUEST_HEADERS)
        self.assertEqual(response.status_code, 400)

    def test_get_method_not_allowed(self):
        # First post one
        response = self.client.post(self.URL, TEST_POST_TRAVEL_TIME['source'], **REQUEST_HEADERS)
        self.assertEqual(response.status_code, 201)

        # Then check if I cannot get it
        response = self.client.get(f'{self.URL}1/', **AUTHORIZATION_HEADER)
        self.assertEqual(response.status_code, 405)

    def test_update_method_not_allowed(self):
        # First post one
        response = self.client.post(self.URL, TEST_POST_TRAVEL_TIME['source'], **REQUEST_HEADERS)
        self.assertEqual(response.status_code, 201)

        # Then check if I cannot update it
        response = self.client.put(f'{self.URL}1/', TEST_POST_TRAVEL_TIME['source'], **REQUEST_HEADERS)
        self.assertEqual(response.status_code, 405)

    def test_delete_method_not_allowed(self):
        # First post one
        response = self.client.post(self.URL, TEST_POST_TRAVEL_TIME['source'], **REQUEST_HEADERS)
        self.assertEqual(response.status_code, 201)

        # Then check if I cannot delete it
        response = self.client.delete(f'{self.URL}1/', **AUTHORIZATION_HEADER)
        self.assertEqual(response.status_code, 405)
