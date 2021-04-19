from datetime import datetime

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

        # assert publication existance and content
        self.assertEqual(Publication.objects.all().count(), 1)
        publication = Publication.objects.get()
        self.assertEqual(publication.type, "travelTime")
        self.assertEqual(publication.reference_id, "PUB_AMS_PRED_TRAJECTORY_TT")
        self.assertEqual(publication.version, "1.0")
        self.assertEqual(
            publication.publication_time,
            datetime.fromisoformat("2019-02-01T12:15:10+00:00"),
        )
        self.assertEqual(
            publication.measurement_start_time,
            datetime.fromisoformat("2019-02-01T12:14:00+00:00"),
        )
        self.assertEqual(
            publication.measurement_end_time,
            datetime.fromisoformat("2019-02-01T12:15:00+00:00"),
        )
        self.assertEqual(publication.measurement_duration, 10)

        self.assertEqual(Measurement.objects.all().count(), 2)
        self.assertEqual(Location.objects.all().count(), 6)
        self.assertEqual(Lane.objects.all().count(), 7)

        # assert traveltime existence and content
        self.assertEqual(TravelTime.objects.all().count(), 5)
        self.assertTrue(
            TravelTime.objects.filter(
                type="predicted",
                estimation_type="estimated",
                travel_time=11,
                traffic_speed=22,
                data_error=False,
                data_quality=None,
                num_input_values_used=None,
            ).exists()
        )
        self.assertTrue(
            TravelTime.objects.filter(
                type="processed",
                estimation_type="estimated",
                travel_time=178,
                traffic_speed=34,
                data_error=True,
                data_quality=38.0,
                num_input_values_used=10,
            ).exists()
        )
        self.assertTrue(
            TravelTime.objects.filter(
                type="raw", travel_time=-1, traffic_speed=-1
            ).exists()
        )
        self.assertTrue(
            TravelTime.objects.filter(
                type="representative", travel_time=-1, traffic_speed=-1
            ).exists()
        )

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

        publication = Publication.objects.get()
        self.assertEqual(publication.type, "travelTime")
        self.assertEqual(publication.reference_id, "IndividualSectionTT_ESB")
        self.assertEqual(publication.version, "1.0")
        self.assertEqual(
            publication.publication_time,
            datetime.fromisoformat("2019-01-22T13:23:40+00:00"),
        )
        self.assertEqual(
            publication.measurement_start_time,
            datetime.fromisoformat("2019-01-22T11:55:00+00:00"),
        )
        self.assertEqual(
            publication.measurement_end_time,
            datetime.fromisoformat("2019-01-22T11:56:00+00:00"),
        )
        self.assertIsNone(publication.measurement_duration)

        self.assertEqual(Measurement.objects.all().count(), 2)
        self.assertEqual(Location.objects.all().count(), 4)
        self.assertEqual(Lane.objects.all().count(), 4)
        self.assertEqual(TravelTime.objects.all().count(), 0)
        self.assertEqual(IndividualTravelTime.objects.all().count(), 3)

        itt = IndividualTravelTime.objects.get(
            license_plate="ABCDEFGHIJKLMNOPQRSTUVWXYZ11111111111111"
        )
        self.assertEqual(itt.vehicle_category.name, "M1")
        self.assertEqual(
            itt.detection_start_time,
            datetime.fromisoformat("2019-01-22T11:55:12+00:00"),
        )
        self.assertEqual(
            itt.detection_end_time,
            datetime.fromisoformat("2019-01-22T11:55:18+00:00"),
        )
        self.assertEqual(itt.travel_time, 1)
        self.assertEqual(itt.traffic_speed, 111)

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
