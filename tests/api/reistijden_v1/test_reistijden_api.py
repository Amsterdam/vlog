from datetime import datetime
from unittest.mock import patch

from django.conf import settings
from django.db.models import Q
from ingress.models import Collection, FailedMessage, Message
from rest_framework.test import APITestCase

from reistijden_v1.consumer import ReistijdenConsumer
from reistijden_v1.models import (
    Camera,
    IndividualTravelTime,
    Lane,
    Measurement,
    MeasurementLocation,
    MeasurementSite,
    Publication,
    TrafficFlow,
    TrafficFlowCategoryCount,
    TravelTime,
)
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


class ReistijdenPostTestBase(APITestCase):
    def setUp(self):
        Collection.objects.get_or_create(name='reistijden_v1', consumer_enabled=True)
        self.URL = '/ingress/reistijden_v1/'


def reraise_current_exception(*_):
    raise


class ReistijdenPostTest(ReistijdenPostTestBase):
    def setUp(self):
        super().setUp()
        # patch the on_consume_error function to reraise the exception so that
        # the test fails with an exception that tells us what went wrong with the
        # processing of the message.
        target = 'ingress.consumer.base.BaseConsumer.on_consume_error'
        self.patcher = patch(target, reraise_current_exception)
        self.patcher.start()

    def tearDown(self):
        super().tearDown()
        self.patcher.stop()

    def test_post_new_travel_time(self):
        # Test posting a new vanilla travel time message
        response = self.client.post(self.URL, TEST_POST_TRAVEL_TIME, **REQUEST_HEADERS)
        self.assertEqual(response.status_code, 200, response.data)

        ReistijdenConsumer().consume(end_at_empty_queue=True)

        # assert publication existence and content
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

        # Assert total counts
        self.assertEqual(Measurement.objects.all().count(), 2)
        self.assertEqual(MeasurementSite.objects.all().count(), 2)
        self.assertEqual(MeasurementLocation.objects.all().count(), 6)
        self.assertEqual(Lane.objects.all().count(), 7)
        self.assertEqual(Camera.objects.all().count(), 7)

        # Assert location, lanes and cameras
        location_qs = MeasurementLocation.objects.filter(
            measurement_site__reference_id="TRJ_1"
        )

        self.assertEqual(location_qs.filter(index=1).count(), 1)
        lanes = location_qs.filter(index=1).get().lane_set
        self.assertEqual(lanes.count(), 2)
        self.assertEqual(lanes.filter(specific_lane='1').get().camera_set.count(), 1)
        self.assertEqual(lanes.filter(specific_lane='2').get().camera_set.count(), 1)
        self.assertTrue(lanes.filter(specific_lane='1').get().camera_set.filter(
            reference_id='233f606b-b5f4-424e-ae2b-266e552ef111',
            latitude=52.111111,
            longitude=4.111111,
            lane_number=1,
            status="on",
            view_direction=111,
        ).exists())

        self.assertEqual(location_qs.filter(index=2).count(), 1)
        lanes = location_qs.filter(index=2).get().lane_set
        self.assertEqual(lanes.filter(specific_lane='1').count(), 1)
        self.assertEqual(lanes.filter(specific_lane='1').get().camera_set.count(), 1)

        self.assertEqual(location_qs.filter(index=3).count(), 1)
        lanes = location_qs.filter(index=3).get().lane_set
        self.assertEqual(lanes.count(), 1)
        self.assertEqual(lanes.get().camera_set.count(), 1)

        self.assertEqual(location_qs.filter(index=4).count(), 1)
        lanes = location_qs.filter(index=4).get().lane_set
        self.assertEqual(lanes.count(), 1)
        self.assertEqual(lanes.get().camera_set.count(), 1)

        # Assert lanes and cameras for second measurement site
        location_qs = MeasurementLocation.objects.filter(
            measurement_site__reference_id="TRJ_2"
        )
        self.assertEqual(location_qs.filter(index=1).count(), 1)
        self.assertEqual(location_qs.filter(index=1).get().lane_set.count(), 1)
        self.assertEqual(location_qs.filter(index=1).get().lane_set.get().camera_set.count(), 1)
        self.assertEqual(location_qs.filter(index=2).count(), 1)
        self.assertEqual(location_qs.filter(index=2).get().lane_set.count(), 1)
        self.assertEqual(location_qs.filter(index=2).get().lane_set.get().camera_set.count(), 1)

        # assert the correct storage of the measurement site details
        measurement_site_qs = MeasurementSite.objects.filter(
                reference_id="TRJ_1",
                name="traject_ZX1",
                version="1.0",
                type="trajectory",
                length=1111,
            )
        self.assertEquals(measurement_site_qs.count(), 1)

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
                type="raw", travel_time=-1, traffic_speed=-1
            ).exists()
        )
        self.assertTrue(
            TravelTime.objects.filter(
                type="representative", travel_time=-1, traffic_speed=-1
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
                type="predicted",
                estimation_type="estimated",
                travel_time=33,
                traffic_speed=44,
                data_error=False,
                data_quality=None,
                num_input_values_used=None,
            ).exists()
        )

        self.assertEqual(IndividualTravelTime.objects.all().count(), 0)
        self.assertEqual(TrafficFlow.objects.all().count(), 0)
        self.assertEqual(TrafficFlowCategoryCount.objects.all().count(), 0)

    def test_post_two_the_same_travel_time_posts(self):
        # Post same travel time twice
        self.client.post(self.URL, TEST_POST_TRAVEL_TIME, **REQUEST_HEADERS)
        self.client.post(self.URL, TEST_POST_TRAVEL_TIME, **REQUEST_HEADERS)

        ReistijdenConsumer().consume(end_at_empty_queue=True)

        # Assert total counts
        self.assertEqual(Publication.objects.all().count(), 2)
        self.assertEqual(Measurement.objects.all().count(), 4)
        self.assertEqual(MeasurementSite.objects.all().count(), 2)
        self.assertEqual(MeasurementLocation.objects.all().count(), 6)
        self.assertEqual(Lane.objects.all().count(), 7)
        self.assertEqual(Camera.objects.all().count(), 7)

    def test_post_new_travel_time_with_adjusted_measurement_site(self):
        # Post first travel time
        self.client.post(self.URL, TEST_POST_TRAVEL_TIME, **REQUEST_HEADERS)

        # Adjust a detail (measurementSiteName) in the posted measurement site and post that
        adjusted_test_post_travel_time = TEST_POST_TRAVEL_TIME.replace("traject_ZX1", 'xxx')
        response = self.client.post(self.URL, adjusted_test_post_travel_time, **REQUEST_HEADERS)
        self.assertEqual(response.status_code, 200, response.data)

        ReistijdenConsumer().consume(end_at_empty_queue=True)

        # Assert total counts
        self.assertEqual(Publication.objects.all().count(), 2)
        self.assertEqual(Measurement.objects.all().count(), 4)
        self.assertEqual(MeasurementSite.objects.all().count(), 3)
        self.assertEqual(MeasurementLocation.objects.all().count(), 10)
        self.assertEqual(Lane.objects.all().count(), 12)
        self.assertEqual(Camera.objects.all().count(), 12)

    def test_post_new_travel_time_with_adjusted_location(self):
        # Post first travel time
        self.client.post(self.URL, TEST_POST_TRAVEL_TIME, **REQUEST_HEADERS)

        # Adjust a detail in the posted locations and post that
        adjusted = TEST_POST_TRAVEL_TIME
        for i in range(1, 5):
            adjusted = adjusted.replace(f'<location index="{i}">', f'<location index="{i}{i}">')
        response = self.client.post(self.URL, adjusted, **REQUEST_HEADERS)
        self.assertEqual(response.status_code, 200, response.data)

        ReistijdenConsumer().consume(end_at_empty_queue=True)

        # Assert total counts
        self.assertEqual(Publication.objects.all().count(), 2)
        self.assertEqual(Measurement.objects.all().count(), 4)
        self.assertEqual(MeasurementSite.objects.all().count(), 4)
        self.assertEqual(MeasurementLocation.objects.all().count(), 12)
        self.assertEqual(Lane.objects.all().count(), 14)
        self.assertEqual(Camera.objects.all().count(), 14)

    def test_post_new_travel_time_with_adjusted_lane(self):
        # Post first travel time
        self.client.post(self.URL, TEST_POST_TRAVEL_TIME, **REQUEST_HEADERS)

        # Adjust a detail in the posted lanes and post that
        adjusted = TEST_POST_TRAVEL_TIME
        for i in range(1, 3):
            adjusted = adjusted.replace(f'<lane specificLane="{i}">', f'<lane specificLane="{i}{i}">')
        response = self.client.post(self.URL, adjusted, **REQUEST_HEADERS)
        self.assertEqual(response.status_code, 200, response.data)

        ReistijdenConsumer().consume(end_at_empty_queue=True)

        # Assert total counts
        self.assertEqual(Publication.objects.all().count(), 2)
        self.assertEqual(Measurement.objects.all().count(), 4)
        self.assertEqual(MeasurementSite.objects.all().count(), 4)
        self.assertEqual(MeasurementLocation.objects.all().count(), 12)
        self.assertEqual(Lane.objects.all().count(), 14)
        self.assertEqual(Camera.objects.all().count(), 14)

    def test_post_new_travel_time_with_adjusted_camera(self):
        # Post first travel time
        self.client.post(self.URL, TEST_POST_TRAVEL_TIME, **REQUEST_HEADERS)

        # Adjust a detail in the posted cameras and post that
        adjusted_test_post_travel_time = TEST_POST_TRAVEL_TIME.replace(
            '<coordinates latitude="52.111111" longitude="4.111111" />',
            '<coordinates latitude="52.111111" longitude="4.111112" />'
        )
        response = self.client.post(self.URL, adjusted_test_post_travel_time, **REQUEST_HEADERS)
        self.assertEqual(response.status_code, 200, response.data)

        ReistijdenConsumer().consume(end_at_empty_queue=True)

        # Assert total counts
        self.assertEqual(Publication.objects.all().count(), 2)
        self.assertEqual(Measurement.objects.all().count(), 4)
        self.assertEqual(MeasurementSite.objects.all().count(), 4)
        self.assertEqual(MeasurementLocation.objects.all().count(), 12)
        self.assertEqual(Lane.objects.all().count(), 14)
        self.assertEqual(Camera.objects.all().count(), 14)


#     def test_post_new_individual_travel_time(self):
#         """Test posting a new vanilla individual travel time message"""
#         response = self.client.post(
#             self.URL, TEST_POST_INDIVIDUAL_TRAVEL_TIME, **REQUEST_HEADERS
#         )
#         self.assertEqual(response.status_code, 200, response.data)
#
#         ReistijdenConsumer().consume(end_at_empty_queue=True)
#
#         self.assertEqual(Publication.objects.all().count(), 1)
#
#         publication = Publication.objects.get()
#         self.assertEqual(publication.type, "travelTime")
#         self.assertEqual(publication.reference_id, "IndividualSectionTT_ESB")
#         self.assertEqual(publication.version, "1.0")
#         self.assertEqual(
#             publication.publication_time,
#             datetime.fromisoformat("2019-01-22T13:23:40+00:00"),
#         )
#         self.assertEqual(
#             publication.measurement_start_time,
#             datetime.fromisoformat("2019-01-22T11:55:00+00:00"),
#         )
#         self.assertEqual(
#             publication.measurement_end_time,
#             datetime.fromisoformat("2019-01-22T11:56:00+00:00"),
#         )
#         self.assertIsNone(publication.measurement_duration)
#
#         self.assertEqual(Measurement.objects.all().count(), 2)
#         self.assertEqual(MeasurementLocation.objects.all().count(), 4)
#         self.assertEqual(Lane.objects.all().count(), 4)
#         self.assertEqual(TravelTime.objects.all().count(), 0)
#         self.assertEqual(IndividualTravelTime.objects.all().count(), 3)
#
#         itt = IndividualTravelTime.objects.get(
#             license_plate="ABCDEFGHIJKLMNOPQRSTUVWXYZ11111111111111"
#         )
#         self.assertEqual(itt.vehicle_category.name, "M1")
#         self.assertEqual(
#             itt.detection_start_time,
#             datetime.fromisoformat("2019-01-22T11:55:12+00:00"),
#         )
#         self.assertEqual(
#             itt.detection_end_time,
#             datetime.fromisoformat("2019-01-22T11:55:18+00:00"),
#         )
#         self.assertEqual(itt.travel_time, 1)
#         self.assertEqual(itt.traffic_speed, 111)
#
#         self.assertEqual(TrafficFlow.objects.all().count(), 0)
#         self.assertEqual(TrafficFlowCategoryCount.objects.all().count(), 0)
#


    def test_post_two_the_same_individual_travel_time_posts(self):
        # Post same travel time twice
        self.client.post(self.URL, TEST_POST_INDIVIDUAL_TRAVEL_TIME, **REQUEST_HEADERS)
        self.client.post(self.URL, TEST_POST_INDIVIDUAL_TRAVEL_TIME, **REQUEST_HEADERS)

        ReistijdenConsumer().consume(end_at_empty_queue=True)

        # Assert total counts
        self.assertEqual(Publication.objects.all().count(), 2)
        self.assertEqual(Measurement.objects.all().count(), 4)
        self.assertEqual(MeasurementSite.objects.all().count(), 2)
        self.assertEqual(MeasurementLocation.objects.all().count(), 4)
        self.assertEqual(Lane.objects.all().count(), 4)
        self.assertEqual(Camera.objects.all().count(), 4)

    def test_post_new_individual_travel_time_with_adjusted_measurement_site(self):
        # Post first travel time
        self.client.post(self.URL, TEST_POST_INDIVIDUAL_TRAVEL_TIME, **REQUEST_HEADERS)

        # Adjust a detail (measurementSite length) in the posted measurement site and post that
        adjusted_test_post = TEST_POST_INDIVIDUAL_TRAVEL_TIME.replace("<length>111", '<length>112')
        response = self.client.post(self.URL, adjusted_test_post, **REQUEST_HEADERS)
        self.assertEqual(response.status_code, 200, response.data)

        ReistijdenConsumer().consume(end_at_empty_queue=True)

        # Assert total counts
        self.assertEqual(Publication.objects.all().count(), 2)
        self.assertEqual(Measurement.objects.all().count(), 4)
        self.assertEqual(MeasurementSite.objects.all().count(), 3)
        self.assertEqual(MeasurementLocation.objects.all().count(), 6)
        self.assertEqual(Lane.objects.all().count(), 6)
        self.assertEqual(Camera.objects.all().count(), 6)

    def test_post_new_individual_travel_time_with_adjusted_location(self):
        # Post first travel time
        self.client.post(self.URL, TEST_POST_INDIVIDUAL_TRAVEL_TIME, **REQUEST_HEADERS)

        # Adjust a detail in the posted locations and post that
        adjusted = TEST_POST_INDIVIDUAL_TRAVEL_TIME
        for i in range(1, 5):
            adjusted = adjusted.replace(f'<location index="{i}">', f'<location index="{i}{i}">')
        response = self.client.post(self.URL, adjusted, **REQUEST_HEADERS)
        self.assertEqual(response.status_code, 200, response.data)

        ReistijdenConsumer().consume(end_at_empty_queue=True)

        # Assert total counts
        self.assertEqual(Publication.objects.all().count(), 2)
        self.assertEqual(Measurement.objects.all().count(), 4)
        self.assertEqual(MeasurementSite.objects.all().count(), 4)
        self.assertEqual(MeasurementLocation.objects.all().count(), 8)
        self.assertEqual(Lane.objects.all().count(), 8)
        self.assertEqual(Camera.objects.all().count(), 8)

    def test_post_new_individual_travel_time_with_adjusted_lane(self):
        # Post first travel time
        self.client.post(self.URL, TEST_POST_INDIVIDUAL_TRAVEL_TIME, **REQUEST_HEADERS)

        # Adjust a detail in the posted lanes and post that
        adjusted = TEST_POST_INDIVIDUAL_TRAVEL_TIME
        for i in range(1, 3):
            adjusted = adjusted.replace(f'<lane specificLane="lane{i}">', f'<lane specificLane="lane{i}{i}">')
        response = self.client.post(self.URL, adjusted, **REQUEST_HEADERS)
        self.assertEqual(response.status_code, 200, response.data)

        ReistijdenConsumer().consume(end_at_empty_queue=True)

        # Assert total counts
        self.assertEqual(Publication.objects.all().count(), 2)
        self.assertEqual(Measurement.objects.all().count(), 4)
        self.assertEqual(MeasurementSite.objects.all().count(), 4)
        self.assertEqual(MeasurementLocation.objects.all().count(), 8)
        self.assertEqual(Lane.objects.all().count(), 8)
        self.assertEqual(Camera.objects.all().count(), 8)

    def test_post_new_individual_travel_time_with_adjusted_camera(self):
        # Post first travel time
        self.client.post(self.URL, TEST_POST_INDIVIDUAL_TRAVEL_TIME, **REQUEST_HEADERS)

        # Adjust a detail in the posted cameras and post that
        adjusted_test_post = TEST_POST_INDIVIDUAL_TRAVEL_TIME.replace(
            '<coordinates latitude="52.111111" longitude="4.111111" />',
            '<coordinates latitude="52.111111" longitude="4.111112" />'
        )
        response = self.client.post(self.URL, adjusted_test_post, **REQUEST_HEADERS)
        self.assertEqual(response.status_code, 200, response.data)

        ReistijdenConsumer().consume(end_at_empty_queue=True)

        # Assert total counts
        self.assertEqual(Publication.objects.all().count(), 2)
        self.assertEqual(Measurement.objects.all().count(), 4)
        self.assertEqual(MeasurementSite.objects.all().count(), 3)
        self.assertEqual(MeasurementLocation.objects.all().count(), 6)
        self.assertEqual(Lane.objects.all().count(), 6)
        self.assertEqual(Camera.objects.all().count(), 6)


#     def test_post_new_individual_travel_time_with_single_measurement(self):
#         """
#         Test posting a new individual travel time message with a single measurement
#         """
#         response = self.client.post(
#             self.URL,
#             TEST_POST_INDIVIDUAL_TRAVEL_TIME_SINGLE_MEASUREMENT,
#             **REQUEST_HEADERS,
#         )
#         self.assertEqual(response.status_code, 200, response.data)
#
#         ReistijdenConsumer().consume(end_at_empty_queue=True)
#
#         self.assertEqual(Publication.objects.all().count(), 1)
#         self.assertEqual(Measurement.objects.all().count(), 1)
#         self.assertEqual(MeasurementLocation.objects.all().count(), 2)
#         self.assertEqual(Lane.objects.all().count(), 2)
#         self.assertEqual(TravelTime.objects.all().count(), 0)
#         self.assertEqual(IndividualTravelTime.objects.all().count(), 2)
#         self.assertEqual(TrafficFlow.objects.all().count(), 0)
#         self.assertEqual(TrafficFlowCategoryCount.objects.all().count(), 0)
#
#     def test_post_new_traffic_flow(self):
#         """Test posting a new vanilla traffic flow message"""
#         response = self.client.post(self.URL, TEST_POST_TRAFFIC_FLOW, **REQUEST_HEADERS)
#         self.assertEqual(response.status_code, 200, response.data)
#
#         ReistijdenConsumer().consume(end_at_empty_queue=True)
#
#         self.assertEqual(Publication.objects.all().count(), 1)
#         self.assertEqual(Measurement.objects.all().count(), 3)
#         self.assertEqual(MeasurementLocation.objects.all().count(), 3)
#         self.assertEqual(Lane.objects.all().count(), 3)
#         self.assertEqual(TravelTime.objects.all().count(), 0)
#         self.assertEqual(IndividualTravelTime.objects.all().count(), 0)
#         self.assertEqual(TrafficFlow.objects.all().count(), 4)
#
#         traffic_flow = TrafficFlow.objects.get(
#             measurement__measurement_site__reference_id=11,
#             specific_lane="lane1",
#             vehicle_flow=6,
#         )
#         self.assertEqual(
#             TrafficFlowCategoryCount.objects.filter(traffic_flow=traffic_flow)
#             .filter(
#                 Q(vehicle_category__name="Auto", count=6)
#                 | Q(vehicle_category__name="Bedrijfsauto Licht", count=2)
#             )
#             .count(),
#             2,
#         )
#
#         traffic_flow = TrafficFlow.objects.get(
#             measurement__measurement_site__reference_id=22,
#             specific_lane="lane1",
#             vehicle_flow=7,
#         )
#         self.assertEqual(
#             TrafficFlowCategoryCount.objects.filter(
#                 traffic_flow=traffic_flow, vehicle_category=None, count=6
#             ).count(),
#             1,
#         )
#
#         traffic_flow = TrafficFlow.objects.get(
#             measurement__measurement_site__reference_id=33,
#             specific_lane="lane1",
#             vehicle_flow=1,
#         )
#         self.assertEqual(
#             TrafficFlowCategoryCount.objects.filter(
#                 traffic_flow=traffic_flow, vehicle_category__name="Auto", count=1
#             ).count(),
#             1,
#         )
#
#         traffic_flow = TrafficFlow.objects.get(
#             measurement__measurement_site__reference_id=33,
#             specific_lane="lane2",
#             vehicle_flow=2,
#         )
#         self.assertEqual(
#             TrafficFlowCategoryCount.objects.filter(
#                 traffic_flow=traffic_flow, vehicle_category__name="Auto", count=2
#             ).count(),
#             1,
#         )
#
#         self.assertEqual(TrafficFlowCategoryCount.objects.all().count(), 5)
#
#     def test_empty_measurement(self):
#         response = self.client.post(self.URL, TEST_POST_EMPTY, **REQUEST_HEADERS)
#         self.assertEqual(response.status_code, 200, response.data)
#
#         ReistijdenConsumer().consume(end_at_empty_queue=True)
#
#         self.assertEqual(Publication.objects.all().count(), 1)
#         self.assertEqual(Measurement.objects.all().count(), 0)
#         self.assertEqual(MeasurementLocation.objects.all().count(), 0)
#         self.assertEqual(Lane.objects.all().count(), 0)
#         self.assertEqual(TravelTime.objects.all().count(), 0)
#         self.assertEqual(IndividualTravelTime.objects.all().count(), 0)
#         self.assertEqual(TrafficFlow.objects.all().count(), 0)
#         self.assertEqual(TrafficFlowCategoryCount.objects.all().count(), 0)
#
#     def test_missing_location_contained_in_itinerary(self):
#         response = self.client.post(
#             self.URL, TEST_POST_MISSING_locationContainedInItinerary, **REQUEST_HEADERS
#         )
#         self.assertEqual(response.status_code, 200, response.data)
#
#         ReistijdenConsumer().consume(end_at_empty_queue=True)
#
#         self.assertEqual(Publication.objects.all().count(), 1)
#         self.assertEqual(Measurement.objects.all().count(), 3)
#         self.assertEqual(MeasurementLocation.objects.all().count(), 2)
#         self.assertEqual(Lane.objects.all().count(), 3)
#         self.assertEqual(TravelTime.objects.all().count(), 9)
#         self.assertEqual(IndividualTravelTime.objects.all().count(), 0)
#         self.assertEqual(TrafficFlow.objects.all().count(), 0)
#         self.assertEqual(TrafficFlowCategoryCount.objects.all().count(), 0)
#
#     def test_post_fails_without_token(self):
#         response = self.client.post(
#             self.URL, TEST_POST_TRAVEL_TIME, **CONTENT_TYPE_HEADER
#         )
#         self.assertEqual(response.status_code, 401, response.data)
#
#
# class ReistijdenPostErrorsTest(ReistijdenPostTestBase):
#     def test_expaterror(self):
#         response = self.client.post(self.URL, TEST_POST_WRONG_TAGS, **REQUEST_HEADERS)
#         self.assertEqual(response.status_code, 200, response.data)
#
#         ReistijdenConsumer().consume(end_at_empty_queue=True)
#
#         self.assertEqual(
#             FailedMessage.objects.filter(
#                 consume_fail_info__icontains='not well-formed (invalid token): '
#                 'line 11, column 5'
#             ).count(),
#             1,
#         )
#         self.assertEqual(Publication.objects.all().count(), 0)
#         self.assertEqual(Measurement.objects.all().count(), 0)
#         self.assertEqual(MeasurementLocation.objects.all().count(), 0)
#         self.assertEqual(Lane.objects.all().count(), 0)
#         self.assertEqual(TravelTime.objects.all().count(), 0)
#         self.assertEqual(IndividualTravelTime.objects.all().count(), 0)
#         self.assertEqual(TrafficFlow.objects.all().count(), 0)
#         self.assertEqual(TrafficFlowCategoryCount.objects.all().count(), 0)
#
#     def test_non_unicode(self):
#         response = self.client.post(self.URL, '\x80abc', **REQUEST_HEADERS)
#         self.assertEqual(response.status_code, 200, response.data)
#
#         ReistijdenConsumer().consume(end_at_empty_queue=True)
#         self.assertEqual(Message.objects.count(), 0)
#         self.assertEqual(FailedMessage.objects.count(), 1)
#
#     def test_post_wrongly_formatted_xml(self):
#         response = self.client.post(
#             self.URL, '<wrongly>formatted</xml>', **REQUEST_HEADERS
#         )
#         self.assertEqual(response.status_code, 200, response.data)
#
#         ReistijdenConsumer().consume(end_at_empty_queue=True)
#         self.assertEqual(Message.objects.count(), 0)
#         self.assertEqual(FailedMessage.objects.count(), 1)
#
#     def test_post_wrongly_formatted_message_structure(self):
#         response = self.client.post(
#             self.URL, '<root>wrong structure</root>', **REQUEST_HEADERS
#         )
#         self.assertEqual(response.status_code, 200, response.data)
#
#         ReistijdenConsumer().consume(end_at_empty_queue=True)
#         self.assertEqual(Message.objects.count(), 0)
#         self.assertEqual(FailedMessage.objects.count(), 1)
