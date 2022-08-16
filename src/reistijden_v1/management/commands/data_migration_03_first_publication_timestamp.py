import logging

from django.core.management import BaseCommand
from django.db import connection

from reistijden_v1.management.commands.util import time_it

logger = logging.getLogger(__name__)


class Command(BaseCommand):
    @time_it('update_first_publication_timestamp')
    def update_first_publication_timestamp(self, batch_size):
        with connection.cursor() as cursor:
            query = """
                with data as (
                    select id, measurement_start_time as first_publication_timestamp
                    from reistijden_v1_measurementsite, lateral (
                        select rv1p.measurement_start_time
                        from reistijden_v1_measurement2 as m
                        join reistijden_v1_publication rv1p on m.publication_id = rv1p.id
                        where m.measurement_site_id=reistijden_v1_measurementsite.id
                        order by m.id
                        limit 1
                    ) as s
                    where first_publication_timestamp is null
                    limit %s
                )
                update reistijden_v1_measurementsite
                set first_publication_timestamp=data.first_publication_timestamp
                from data
                where reistijden_v1_measurementsite.id=data.id
            """
            cursor.execute(query, (batch_size,))
            return cursor.rowcount

    def add_arguments(self, parser):
        parser.add_argument('--batch-size', type=int, default=100)

    @time_it('handle')
    def handle(self, *args, **options):
        batch_size = options['batch_size']
        while self.update_first_publication_timestamp(batch_size):
            pass
