from io import StringIO

import pytest
from django.db import connection
from django.utils.timezone import now
from reistijden_v1.management.commands.data_migration_02_measurement_sites import (
    Command,
)

from .test_data_migration import TestDataMigrationBase


@pytest.mark.django_db
class TestDataMigration(TestDataMigrationBase):

    migrate_from = ('reistijden_v1', '0001_initial')
    migrate_to = ('reistijden_v1', '0011_02_measurement_sites')

    def setUp(self):
        super().setUp()

        keys = 'publication_time', 'measurement_start_time', 'measurement_end_time'
        (publication,) = self.create_objects('Publication', dict.fromkeys(keys, now()))

        # create some Measurement objects
        default_values = dict(publication=publication, type='section', version='1.0')
        self.create_objects(
            'Measurement',
            dict(default_values, reference_id='SEC_0001', name='abcd', length=0),
            dict(default_values, reference_id='SEC_0001', name='abcd', length=None),
            dict(default_values, reference_id='SEC_0002', name='xyz', length=0),
            dict(default_values, reference_id='SEC_0002', name='xyz', length=42),
        )

        self.finish_schema_migration()

    def test_migration(self):
        self.call_command(Command)
        fields = 'reference_id', 'version', 'name', 'type', 'length'
        values_list = self.get_model('MeasurementSite').objects.values_list
        actual = sorted(values_list('id', *fields))
        values_list = self.get_model('Measurement').objects.values_list
        expected = sorted(values_list('measurement_site_id', *fields))
        self.assertEqual(actual, expected)

    def test_validation(self):

        with connection.cursor() as cursor:

            command = Command()
            command.stdout = StringIO()
            command.migrate(cursor)

            # introduce some errors into the migrated data
            MeasurementSite = self.get_model('MeasurementSite')
            measurement_site = MeasurementSite.objects.get(
                reference_id='SEC_0001',
                length=0,
            )
            measurement_site.reference_id = 'foobar'
            measurement_site.save()
            measurement_site = MeasurementSite.objects.get(
                reference_id='SEC_0002',
                length=0,
            )
            measurement_site.length = None
            measurement_site.save()

            # validate and check that the error was detected.
            expected, errors = command.validate(cursor)
            self.assertEqual(expected, 4)
            self.assertEqual(errors, 2)
