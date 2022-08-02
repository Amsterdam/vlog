import logging

from django.core.management import BaseCommand
from django.db import connection

from reistijden_v1.management.commands.util import time_it

logger = logging.getLogger(__name__)


class Command(BaseCommand):
    @time_it('insert_vehicle_categories')
    def handle(self, *args, **options):
        with connection.cursor() as cursor:
            cursor.execute(
                """
                INSERT INTO reistijden_v1_vehiclecategory (name)
                SELECT type
                FROM reistijden_v1_trafficflowcategorycount
                WHERE type IS NOT NULL
                UNION
                SELECT vehicle_category
                FROM reistijden_v1_individualtraveltime
                WHERE vehicle_category IS NOT NULL
                ON CONFLICT DO NOTHING
            """
            )
