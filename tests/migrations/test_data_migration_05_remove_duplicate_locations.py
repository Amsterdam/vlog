import pytest
from reistijden_v1.management.commands.data_migration_05_remove_duplicate_locations import (  # noqa
    Command,
)

from .test_data_migration import TestDataMigrationBase


@pytest.mark.django_db
class TestDataMigration(TestDataMigrationBase):

    migrate_from = ('reistijden_v1', '0001_initial')
    migrate_to = ('reistijden_v1', '0014_05_cameras_from_lanes')

    def setUp(self):
        super().setUp()

        measurement_sites = self.create_objects('MeasurementSite', {}, {})
        self.measurement_locations = self.create_objects(
            'MeasurementLocation',
            dict(measurement_site=measurement_sites[0], index=1),
            dict(measurement_site=measurement_sites[1], index=2),
        )
        self.create_objects(
            'Lane',
            *[
                dict(
                    measurement_location=location,
                    specific_lane='1',
                    camera_id='1',
                    latitude=1,
                    longitude=1,
                    lane_number=1,
                    status='',
                    view_direction=0,
                )
                for location in self.measurement_locations
                for i in range(3)
            ]
        )

    def test_migration(self):
        self.call_command(Command)
        values_list = self.get_model('MeasurementLocation').objects.values_list
        actual = sorted(values_list('id'))
        values_list = self.get_model('Lane').objects.values_list
        expected = sorted(values_list('measurement_location_id'))
        self.assertEqual(actual, expected)
