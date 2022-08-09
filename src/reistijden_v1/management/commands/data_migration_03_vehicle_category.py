import logging

from django.core.management import BaseCommand
from django.db import connection

from reistijden_v1.management.commands.util import time_it

logger = logging.getLogger(__name__)


class Command(BaseCommand):

    @time_it('insert_vehicle_categories')
    def insert_vehicle_categories(self):
        with connection.cursor() as cursor:
            cursor.execute(
                """
                INSERT INTO reistijden_v1_vehiclecategory (name)
                SELECT type
                FROM reistijden_v1_trafficflowcategorycount
                WHERE type IS NOT NULL
                UNION
                SELECT old_vehicle_category
                FROM reistijden_v1_individualtraveltime
                WHERE old_vehicle_category IS NOT NULL
                ON CONFLICT DO NOTHING
            """
            )

    @time_it('update_individual_travel_time')
    def update_individual_travel_time(self):
        with connection.cursor() as cursor:
            cursor.execute(
                """
                UPDATE reistijden_v1_individualtraveltime
                SET vehicle_category_id=reistijden_v1_vehiclecategory.id
                FROM reistijden_v1_vehiclecategory
                WHERE old_vehicle_category=name
            """
            )

    @time_it('update_traffic_flow_category_count')
    def update_traffic_flow_category_count(self):
        with connection.cursor() as cursor:
            cursor.execute(
                """
                UPDATE reistijden_v1_trafficflowcategorycount
                SET vehicle_category_id=reistijden_v1_vehiclecategory.id
                FROM reistijden_v1_vehiclecategory
                WHERE type=name
            """
            )

    def handle(self, *args, **options):
        self.insert_vehicle_categories()
        self.update_individual_travel_time()
        self.update_individual_travel_time()
