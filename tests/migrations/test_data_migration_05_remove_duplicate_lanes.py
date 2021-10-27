import itertools

import pytest
from django.utils.timezone import now
from reistijden_v1.management.commands.data_migration_05_cameras_from_lanes import (  # noqa
    Command,
)

from .test_data_migration import TestDataMigrationBase


@pytest.mark.django_db
class TestDataMigration(TestDataMigrationBase):

    migrate_from = ('reistijden_v1', '0001_initial')
    migrate_to = ('reistijden_v1', '0014_05_cameras_from_lanes')

    def setUp(self):
        super().setUp()

        keys = 'publication_time', 'measurement_start_time', 'measurement_end_time'
        (publication,) = self.create_objects('Publication', dict.fromkeys(keys, now()))
        measurement_sites = self.create_objects('MeasurementSite', {}, {}, {})
        measurements = self.create_objects(
            'Measurement',
            dict(publication=publication, measurement_site=None),
            dict(publication=publication, measurement_site=measurement_sites[0]),
            dict(publication=publication, measurement_site=measurement_sites[1]),
            dict(publication=publication, measurement_site=measurement_sites[2]),
        )
        self.measurement_locations = self.create_objects(
            'MeasurementLocation',
            dict(measurement=measurements[0], index=1),
            dict(measurement=measurements[0], index=2),
            dict(measurement=measurements[1], index=1),
            dict(measurement=measurements[1], index=2),
            dict(measurement=measurements[2], index=1),
            dict(measurement=measurements[2], index=2),
        )
        self.create_objects(
            'Lane',
            *(
                dict(
                    measurement_location=measurement_location,
                    specific_lane=str(lane_number),
                    camera_id=f'{lat}_{long}_{lane_number}',
                    latitude=lat,
                    longitude=long,
                    lane_number=lane_number,
                    status='',
                    view_direction=0,
                )
                for measurement_location in self.measurement_locations
                for lat, long, lane_number in itertools.combinations(range(4), 3)
            ),
        )

    def test_migration(self):
        self.call_command(Command)
        values_list = self.get_model('Lane').objects.values_list
        actual = sorted(values_list('id'))
        values_list = self.get_model('Camera').objects.values_list
        expected = sorted(values_list('lane_id'))
        self.assertEqual(actual, expected)
