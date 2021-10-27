from io import StringIO

import pytest
from django.db import connection
from django.utils.timezone import now
from reistijden_v1.management.commands.data_migration_03_traffic_flow_category_count_vehicle_categories import (  # noqa
    Command,
)

from .test_data_migration import TestDataMigrationBase


@pytest.mark.django_db
class TestDataMigration(TestDataMigrationBase):

    migrate_from = ('reistijden_v1', '0001_initial')
    migrate_to = (
        'reistijden_v1',
        '0012_03_traffic_flow_category_count_vehicle_categories',
    )

    def setUp(self):
        super().setUp()

        keys = 'publication_time', 'measurement_start_time', 'measurement_end_time'
        (publication,) = self.create_objects('Publication', dict.fromkeys(keys, now()))
        (measurement,) = self.create_objects(
            'Measurement', dict(publication=publication)
        )
        (traffic_flow,) = self.create_objects(
            'TrafficFlow',
            dict(measurement=measurement, vehicle_flow=0),
        )

        # Create some objects to migrate
        self.create_objects(
            'TrafficFlowCategoryCount',
            dict(type='abc', traffic_flow=traffic_flow, count=0),
            dict(type='xyz', traffic_flow=traffic_flow, count=0),
            dict(type='', traffic_flow=traffic_flow, count=0),
        )

        # create a VehicleCategory to check we don't insert duplicate values
        self.create_objects('VehicleCategory', dict(name='abc'))

        self.finish_schema_migration()

    def test_migration(self):
        self.call_command(Command)
        values_list = self.get_model('VehicleCategory').objects.values_list
        actual = sorted(values_list('name', 'id'))
        values_list = self.get_model('TrafficFlowCategoryCount').objects.values_list
        expected = sorted(values_list('type', 'vehicle_category_id'))
        self.assertEqual(actual, expected)

    def test_validation(self):

        with connection.cursor() as cursor:

            command = Command()
            command.stdout = StringIO()
            command.migrate(cursor)

            # introduce some errors into the migrated data
            VehicleCategory = self.get_model('VehicleCategory')
            vehicle_category = VehicleCategory.objects.get(name='xyz')
            vehicle_category.name = 'mno'
            vehicle_category.save()

            # validate and check that the error was detected.
            expected, errors = command.validate(cursor)
            self.assertEqual(expected, 3)
            self.assertEqual(errors, 1)
