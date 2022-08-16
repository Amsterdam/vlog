import logging

from django.core.management import BaseCommand
from django.db import connection

from reistijden_v1.management.commands.util import time_it

logger = logging.getLogger(__name__)


class Command(BaseCommand):

    @time_it('update_created_timestamp')
    def update_created_timestamp(self):
        with connection.cursor() as cursor:
            cursor.execute(
                """
                with data as (
                    select id, measurement_start_time as created_timestamp
                    from reistijden_v1_measurementsite, lateral (
                        select rv1p.measurement_start_time
                        from reistijden_v1_measurement2 as m
                        join reistijden_v1_publication rv1p on m.publication_id = rv1p.id
                        where m.measurement_site_id=reistijden_v1_measurementsite.id
                        order by m.id
                        limit 1
                    ) as s
                    where created_timestamp is null
                    limit 100
                )
                update reistijden_v1_measurementsite
                set created_timestamp=timestamp.created_timestamp
                from data
                where reistijden_v1_measurementsite.id=data.id
            """
            )
            return cursor.rowcount

    @time_it('handle')
    def handle(self, *args, **options):
        while self.update_created_timestamp():
            pass