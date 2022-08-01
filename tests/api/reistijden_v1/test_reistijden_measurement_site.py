from io import StringIO

import pytest
from django.test import TestCase

from reistijden_v1.models import Camera, Lane2, MeasurementLocation2, MeasurementSite


@pytest.mark.django_db
class MeasurementSiteTest(TestCase):

    BASE_MEASUREMENT_SITE = {
        'name': 'foobar',
        'type': 'trajectory',
        'length': 2736,
        'version': '1.0',
        'reference_id': 'foobar',
        'measurement_locations': [
            {
                'index': 1,
                'lanes': [
                    {
                        'cameras': [
                            {
                                'status': 'on',
                                'latitude': 52.372334,
                                'reference_id': '322aac3d-62c2-495b-afee-7deded30f0e7',
                                'longitude': 4.961688,
                                'lane_number': -1,
                                'view_direction': 112,
                            }
                        ],
                        'specific_lane': '-1',
                    }
                ],
            }
        ],
    }

    def measurement_site_test(self, expected_count_after, measurement_site_json):
        """
        Calls MeasurementSite.get_or_create twice, once with BASE_MEASUREMENT_SITE
        and then again with measurement_site_json, checking the expected count after
        the second call.
        """
        self.assertEqual(MeasurementSite.objects.count(), 0)
        self.assertEqual(MeasurementLocation2.objects.count(), 0)
        self.assertEqual(Lane2.objects.count(), 0)
        self.assertEqual(Camera.objects.count(), 0)

        MeasurementSite.get_or_create(self.BASE_MEASUREMENT_SITE)

        self.assertEqual(MeasurementSite.objects.count(), 1)
        self.assertEqual(MeasurementLocation2.objects.count(), 1)
        self.assertEqual(Lane2.objects.count(), 1)
        self.assertEqual(Camera.objects.count(), 1)

        MeasurementSite.get_or_create(measurement_site_json)

        self.assertEqual(MeasurementSite.objects.count(), expected_count_after)
        self.assertEqual(MeasurementLocation2.objects.count(), expected_count_after)
        self.assertEqual(Lane2.objects.count(), expected_count_after)
        self.assertEqual(Camera.objects.count(), expected_count_after)

    def test_changes_in_measurement_site_should_lead_to_new_measurement_site(self):
        self.measurement_site_test(
            2,
            {
                'name': 'foobar',
                'type': 'trajectory',
                'length': 5000,  # different vs BASE_MEASUREMENT_SITE
                'version': '1.0',
                'reference_id': 'foobar',
                'measurement_locations': [
                    {
                        'index': 1,
                        'lanes': [
                            {
                                'cameras': [
                                    {
                                        'status': 'on',
                                        'latitude': 52.372334,
                                        'reference_id': '322aac3d-62c2-495b-afee-7deded30f0e7',
                                        'longitude': 4.961688,
                                        'lane_number': -1,
                                        'view_direction': 112,
                                    }
                                ],
                                'specific_lane': '-1',
                            }
                        ],
                    }
                ],
            },
        )

    def test_changes_in_locations_should_lead_to_new_measurement_site(self):
        self.measurement_site_test(
            2,
            {
                'name': 'foobar',
                'type': 'trajectory',
                'length': 2736,
                'version': '1.0',
                'reference_id': 'foobar',
                'measurement_locations': [
                    {
                        'index': 2,  # different vs BASE_MEASUREMENT_SITE
                        'lanes': [
                            {
                                'cameras': [
                                    {
                                        'status': 'on',
                                        'latitude': 52.372334,
                                        'reference_id': '322aac3d-62c2-495b-afee-7deded30f0e7',
                                        'longitude': 4.961688,
                                        'lane_number': -1,
                                        'view_direction': 112,
                                    }
                                ],
                                'specific_lane': '-1',
                            }
                        ],
                    }
                ],
            },
        )

    def test_changes_in_lanes_should_lead_to_new_measurement_site(self):
        self.measurement_site_test(
            2,
            {
                'name': 'foobar',
                'type': 'trajectory',
                'length': 2736,
                'version': '1.0',
                'reference_id': 'foobar',
                'measurement_locations': [
                    {
                        'index': 1,
                        'lanes': [
                            {
                                'cameras': [
                                    {
                                        'status': 'on',
                                        'latitude': 52.372334,
                                        'reference_id': '322aac3d-62c2-495b-afee-7deded30f0e7',
                                        'longitude': 4.961688,
                                        'lane_number': -1,
                                        'view_direction': 112,
                                    }
                                ],
                                'specific_lane': 'lane1',  # different vs BASE_MEASUREMENT_SITE
                            }
                        ],
                    }
                ],
            },
        )

    def test_changes_in_cameras_should_lead_to_new_measurement_site(self):
        self.measurement_site_test(
            2,
            {
                'name': 'foobar',
                'type': 'trajectory',
                'length': 2736,
                'version': '1.0',
                'reference_id': 'foobar',
                'measurement_locations': [
                    {
                        'index': 1,
                        'lanes': [
                            {
                                'cameras': [
                                    {
                                        'status': 'on',
                                        'latitude': 52.372334,
                                        'reference_id': '322aac3d-62c2-495b-afee-7deded30f0e7',
                                        'longitude': 4.961688,
                                        'lane_number': -1,
                                        'view_direction': 200,  # different vs BASE_MEASUREMENT_SITE
                                    }
                                ],
                                'specific_lane': '-1',
                            }
                        ],
                    }
                ],
            },
        )

    def test_no_changes_should_not_lead_to_new_measurement_site(self):
        self.measurement_site_test(1, self.BASE_MEASUREMENT_SITE)

    def test_different_ordering_of_keys_should_not_lead_to_new_measurement_site(self):
        self.measurement_site_test(
            1,
            {
                # keys in different order vs BASE_MEASUREMENT_SITE
                'reference_id': 'foobar',
                'version': '1.0',
                'length': 2736,
                'type': 'trajectory',
                'name': 'foobar',
                'measurement_locations': [
                    {
                        'index': 1,
                        'lanes': [
                            {
                                'cameras': [
                                    {
                                        'status': 'on',
                                        'latitude': 52.372334,
                                        'reference_id': '322aac3d-62c2-495b-afee-7deded30f0e7',
                                        'longitude': 4.961688,
                                        'lane_number': -1,
                                        'view_direction': 112,
                                    }
                                ],
                                'specific_lane': '-1',
                            }
                        ],
                    }
                ],
            },
        )
