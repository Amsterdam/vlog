from django.conf import settings
from ingress.models import Collection, FailedMessage, Message
from reistijden_v1.consumer import ReistijdenConsumer
from reistijden_v1.models import (
    Category,
    IndividualTravelTime,
    Lane,
    Location,
    MeasuredFlow,
    Measurement,
    Publication,
    TravelTime,
)
from rest_framework.test import APITestCase

from tests.api.reistijden_v1.test_xml import (
    TEST_POST_EMPTY,
    TEST_POST_INDIVIDUAL_TRAVEL_TIME,
    TEST_POST_INDIVIDUAL_TRAVEL_TIME_SINGLE_MEASUREMENT,
    TEST_POST_TRAFFIC_FLOW,
    TEST_POST_TRAVEL_TIME,
    TEST_POST_WRONG_TAGS,
    TEST_POST_MISSING_locationContainedInItinerary,
)

AUTHORIZATION_HEADER = {'HTTP_AUTHORIZATION': f"Token {settings.AUTHORIZATION_TOKEN}"}
CONTENT_TYPE_HEADER = {'content_type': 'application/xml'}
REQUEST_HEADERS = {**AUTHORIZATION_HEADER, **CONTENT_TYPE_HEADER}


class ReistijdenPostTest(APITestCase):
    def setUp(self):
        Collection.objects.get_or_create(name='reistijden_v1', consumer_enabled=True)
        self.URL = '/ingress/reistijden_v1/'

    def test_post_new_travel_time(self):
        """ Test posting a new vanilla travel time message """
        response = self.client.post(self.URL, TEST_POST_TRAVEL_TIME, **REQUEST_HEADERS)
        self.assertEqual(response.status_code, 200, response.data)

        ReistijdenConsumer().consume(end_at_empty_queue=True)

        self.assertEqual(Publication.objects.all().count(), 1)
        self.assertEqual(Measurement.objects.all().count(), 2)
        self.assertEqual(Location.objects.all().count(), 6)
        self.assertEqual(Lane.objects.all().count(), 7)
        self.assertEqual(TravelTime.objects.all().count(), 5)
        self.assertEqual(IndividualTravelTime.objects.all().count(), 0)
        self.assertEqual(MeasuredFlow.objects.all().count(), 0)
        self.assertEqual(Category.objects.all().count(), 0)

    def test_post_new_individual_travel_time(self):
        """ Test posting a new vanilla individual travel time message """
        response = self.client.post(
            self.URL, TEST_POST_INDIVIDUAL_TRAVEL_TIME, **REQUEST_HEADERS
        )
        self.assertEqual(response.status_code, 200, response.data)

        ReistijdenConsumer().consume(end_at_empty_queue=True)

        self.assertEqual(Publication.objects.all().count(), 1)
        self.assertEqual(Measurement.objects.all().count(), 2)
        self.assertEqual(Location.objects.all().count(), 4)
        self.assertEqual(Lane.objects.all().count(), 4)
        self.assertEqual(TravelTime.objects.all().count(), 0)
        self.assertEqual(IndividualTravelTime.objects.all().count(), 3)
        self.assertEqual(MeasuredFlow.objects.all().count(), 0)
        self.assertEqual(Category.objects.all().count(), 0)

    def test_post_new_individual_travel_time_with_single_measurement(self):
        """
        Test posting a new individual travel time message with a single measurement
        """
        response = self.client.post(
            self.URL,
            TEST_POST_INDIVIDUAL_TRAVEL_TIME_SINGLE_MEASUREMENT,
            **REQUEST_HEADERS,
        )
        self.assertEqual(response.status_code, 200, response.data)

        ReistijdenConsumer().consume(end_at_empty_queue=True)

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
        self.assertEqual(response.status_code, 200, response.data)

        ReistijdenConsumer().consume(end_at_empty_queue=True)

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
        self.assertEqual(response.status_code, 200, response.data)

        ReistijdenConsumer().consume(end_at_empty_queue=True)

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
        self.assertEqual(response.status_code, 200, response.data)

        ReistijdenConsumer().consume(end_at_empty_queue=True)

        self.assertEqual(
            FailedMessage.objects.filter(
                consume_fail_info__icontains='not well-formed (invalid token): '
                'line 11, column 5'
            ).count(),
            1,
        )
        self.assertEqual(Publication.objects.all().count(), 0)
        self.assertEqual(Measurement.objects.all().count(), 0)
        self.assertEqual(Location.objects.all().count(), 0)
        self.assertEqual(Lane.objects.all().count(), 0)
        self.assertEqual(TravelTime.objects.all().count(), 0)
        self.assertEqual(IndividualTravelTime.objects.all().count(), 0)
        self.assertEqual(MeasuredFlow.objects.all().count(), 0)
        self.assertEqual(Category.objects.all().count(), 0)

    def test_missing_location_contained_in_itinerary(self):
        response = self.client.post(
            self.URL, TEST_POST_MISSING_locationContainedInItinerary, **REQUEST_HEADERS
        )
        self.assertEqual(response.status_code, 200, response.data)

        ReistijdenConsumer().consume(end_at_empty_queue=True)

        self.assertEqual(Publication.objects.all().count(), 1)
        self.assertEqual(Measurement.objects.all().count(), 3)
        self.assertEqual(Location.objects.all().count(), 2)
        self.assertEqual(Lane.objects.all().count(), 3)
        self.assertEqual(TravelTime.objects.all().count(), 9)
        self.assertEqual(IndividualTravelTime.objects.all().count(), 0)
        self.assertEqual(MeasuredFlow.objects.all().count(), 0)
        self.assertEqual(Category.objects.all().count(), 0)

    def test_post_fails_without_token(self):
        response = self.client.post(
            self.URL, TEST_POST_TRAVEL_TIME, **CONTENT_TYPE_HEADER
        )
        self.assertEqual(response.status_code, 401, response.data)

    def test_post_wrongly_formatted_xml(self):
        response = self.client.post(
            self.URL, '<wrongly>formatted</xml>', **REQUEST_HEADERS
        )
        self.assertEqual(response.status_code, 200, response.data)

        ReistijdenConsumer().consume(end_at_empty_queue=True)
        self.assertEqual(Message.objects.count(), 0)
        self.assertEqual(FailedMessage.objects.count(), 1)

    def test_post_wrongly_formatted_message_structure(self):
        response = self.client.post(
            self.URL, '<root>wrong structure</root>', **REQUEST_HEADERS
        )
        self.assertEqual(response.status_code, 200, response.data)

        ReistijdenConsumer().consume(end_at_empty_queue=True)
        self.assertEqual(Message.objects.count(), 0)
        self.assertEqual(FailedMessage.objects.count(), 1)

    def test_non_unicode(self):
        response = self.client.post(self.URL, '\x80abc', **REQUEST_HEADERS)
        self.assertEqual(response.status_code, 200, response.data)

        ReistijdenConsumer().consume(end_at_empty_queue=True)
        self.assertEqual(Message.objects.count(), 0)
        self.assertEqual(FailedMessage.objects.count(), 1)
