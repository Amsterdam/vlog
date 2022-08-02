import pytest
from django.test import TestCase

from reistijden_v1.models import Camera, Lane, MeasurementLocation, MeasurementSite


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

    def _measurement_site_test(self, before, after, *, expect_new: bool):
        """
        Calls MeasurementSite.get_or_create twice, once with before json and then
        again with after, depending on the value of expect_new we either check
        if the counts of the objects are the same (i.e. no new measurement site
        was created, expect_new == False) or that they are different (i.e. a
        new measurement site was created, expect_new == True).
        """
        self.assertEqual(MeasurementSite.objects.count(), 0)
        self.assertEqual(MeasurementLocation.objects.count(), 0)
        self.assertEqual(Lane.objects.count(), 0)
        self.assertEqual(Camera.objects.count(), 0)

        MeasurementSite.get_or_create(before)

        measurement_site_count = MeasurementSite.objects.count()
        measurement_location_count = MeasurementLocation.objects.count()
        lane_count = Lane.objects.count()
        camera_count = Camera.objects.count()

        MeasurementSite.get_or_create(after)

        # The counts before and after the second call should not be equal if we
        # expect the second call to create a new measurement site, otherwise we
        # expect the counts to remain the same
        assertion = self.assertNotEqual if expect_new else self.assertEqual

        assertion(measurement_site_count, MeasurementSite.objects.count())
        assertion(measurement_location_count, MeasurementLocation.objects.count())
        assertion(lane_count, Lane.objects.count())
        assertion(camera_count, Camera.objects.count())

    def test_changes_in_measurement_site_should_lead_to_new_measurement_site(self):
        before = self.BASE_MEASUREMENT_SITE
        after = {
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
                },
            ],
        }
        self._measurement_site_test(before, after, expect_new=True)

    def test_changes_in_locations_should_lead_to_new_measurement_site(self):
        before = self.BASE_MEASUREMENT_SITE
        after = {
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
        }
        self._measurement_site_test(before, after, expect_new=True)

    def test_changes_in_lanes_should_lead_to_new_measurement_site(self):
        before = self.BASE_MEASUREMENT_SITE
        after = {
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
        }
        self._measurement_site_test(before, after, expect_new=True)

    def test_changes_in_cameras_should_lead_to_new_measurement_site(self):
        before = self.BASE_MEASUREMENT_SITE
        after = {
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
        }
        self._measurement_site_test(before, after, expect_new=True)

    def test_no_changes_should_not_lead_to_new_measurement_site(self):
        before = self.BASE_MEASUREMENT_SITE
        after = self.BASE_MEASUREMENT_SITE
        self._measurement_site_test(before, after, expect_new=False)

    def test_different_ordering_of_keys_should_not_lead_to_new_measurement_site(self):
        before = self.BASE_MEASUREMENT_SITE
        after = {
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
        }
        self._measurement_site_test(before, after, expect_new=False)

    # measurement site with multiple locations, lanes and cameras, all
    # of which are in an unnatural order. we can use this to check that
    # different ordering does not end up creating new measurement sites
    UNORDERED_MEASUREMENT_SITE = {
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
            },
            {
                'index': 2,
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
                        'specific_lane': '-2',
                    },
                    {
                        'cameras': [
                            {
                                'status': 'on',
                                'latitude': 52.372334,
                                'reference_id': '322aac3d-62c2-495b-afee-7deded30f0e7',
                                'longitude': 4.961688,
                                'lane_number': -1,
                                'view_direction': 999,
                            },
                            {
                                'status': 'on',
                                'latitude': 52.372334,
                                'reference_id': '322aac3d-62c2-495b-afee-7deded30f0e7',
                                'longitude': 4.961688,
                                'lane_number': -1,
                                'view_direction': 112,
                            },
                        ],
                        'specific_lane': '-1',
                    },
                ],
            },
        ],
    }

    def test_different_order_should_not_lead_to_new_measurement_site(self):
        before = self.UNORDERED_MEASUREMENT_SITE
        # lists are in the correct order vs UNORDERED_MEASUREMENT_SITE
        after = {
            'name': 'foobar',
            'type': 'trajectory',
            'length': 2736,
            'version': '1.0',
            'reference_id': 'foobar',
            'measurement_locations': [
                {
                    'index': 2,
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
                                },
                                {
                                    'status': 'on',
                                    'latitude': 52.372334,
                                    'reference_id': '322aac3d-62c2-495b-afee-7deded30f0e7',
                                    'longitude': 4.961688,
                                    'lane_number': -1,
                                    'view_direction': 999,
                                },
                            ],
                            'specific_lane': '-1',
                        },
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
                            'specific_lane': '-2',
                        },
                    ],
                },
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
                },
            ],
        }
        self._measurement_site_test(before, after, expect_new=False)
