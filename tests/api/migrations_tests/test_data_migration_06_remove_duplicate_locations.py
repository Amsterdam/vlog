import pytest
from django.utils.timezone import now
from reistijden_v1.management.commands.data_migration_06_remove_duplicate_locations import (  # noqa
    Command,
)

from tests.api.migrations_tests.test_data_migration import TestDataMigration


@pytest.mark.django_db
class TestVehicleCategoryDataMigration(TestDataMigration):

    migrate_from = ('reistijden_v1', '0001_initial')
    migrate_to = ('reistijden_v1', '0014_05_remove_duplicate_lanes')

    def setUp(self):
        super().setUp()

        keys = 'publication_time', 'measurement_start_time', 'measurement_end_time'
        publication, = self.create_objects('Publication', dict.fromkeys(keys, now()))
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
        )
        self.create_objects(
            'Lane',
            dict(
                measurement_location=self.measurement_locations[0],
                specific_lane='1',
                camera_id='1',
                latitude=1,
                longitude=1,
                lane_number=1,
                status='',
                view_direction=0,
            )
        )

    def test_migration(self):
        self.call_command(Command)
        values_list = self.get_model('MeasurementLocation').objects.values_list
        actual = sorted(values_list('id'))
        values_list = self.get_model('Lane').objects.values_list
        expected = sorted(values_list('measurement_location_id'))
        self.assertEqual(actual, expected)
