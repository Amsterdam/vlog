import pytest
from django.db import connection
from django.utils.timezone import now
from reistijden_v1.management.commands.data_migration_04_measurement_location_site_id import (  # noqa
    Command,
)

from tests.api.migrations_tests.test_data_migration import TestDataMigration


@pytest.mark.django_db
class TestVehicleCategoryDataMigration(TestDataMigration):

    migrate_from = ('reistijden_v1', '0001_initial')
    migrate_to = ('reistijden_v1', '0013_04_measurement_location_site_id')

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
            dict(measurement=measurements[1], index=1),
            dict(measurement=measurements[1], index=2),
            dict(measurement=measurements[2], index=1),
            dict(measurement=measurements[2], index=2),
        )

    def test_migration(self):
        self.call_command(Command)
        values_list = self.get_model('MeasurementLocation').objects.values_list
        actual = sorted(values_list('id', 'measurement_site_id'))
        expected = sorted(values_list('id', 'measurement__measurement_site_id'))
        self.assertEqual(actual, expected)

    def test_validation(self):

        with connection.cursor() as cursor:

            command = Command()
            command.migrate(cursor)

            # introduce some errors into the migrated data
            self.measurement_locations[2].measurement_site_id = None
            self.measurement_locations[2].save()

            # validate and check that the error was detected.
            expected, errors = command.validate(cursor)
            self.assertEqual(expected, 6)
            self.assertEqual(errors, 1)
