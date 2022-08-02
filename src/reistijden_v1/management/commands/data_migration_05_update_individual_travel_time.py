import logging

from django.core.management import BaseCommand
from django.db import connection

from reistijden_v1.management.commands.util import time_it

logger = logging.getLogger(__name__)


class Command(BaseCommand):
    @time_it('update_individual_travel_time')
    def handle(self, *args, **options):
        with connection.cursor() as cursor:
            cursor.execute(
                """
                UPDATE reistijden_v1_individualtraveltime
                SET vehicle_category_id=reistijden_v1_vehiclecategory.id
                FROM reistijden_v1_vehiclecategory
                WHERE vehicle_category=name
            """
            )
