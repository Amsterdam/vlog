import logging

from django.core.management import BaseCommand
from django.db import connection

from reistijden_v1.management.commands.util import time_it

logger = logging.getLogger(__name__)


class Command(BaseCommand):
    @time_it('update_traffic_flow_category_count')
    def handle(self, *args, **options):
        with connection.cursor() as cursor:
            cursor.execute(
                """
                UPDATE reistijden_v1_trafficflowcategorycount
                SET vehicle_category_id=reistijden_v1_vehiclecategory.id
                FROM reistijden_v1_vehiclecategory
                WHERE type=name
            """
            )
