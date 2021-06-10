import logging

from django.core.management import BaseCommand

from reistijden_v1.models import MeasurementLocation

logger = logging.getLogger(__name__)


class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument('--sleep', nargs='?', default=1, type=int)

    def handle(self, **options):
        logger.info("message")

        sleep = options['sleep']

        measurement_locations = MeasurementLocation.objects.all().select_related(
            'measurement'
        )
        for location in measurement_locations:
            location.measurement_site_id = location.measurement.measurement_site_id

        MeasurementLocation.objects.bulk_update(
            measurement_locations, fields=['measurement_site_id'], batch_size=1000
        )

        self.stdout.write(self.style.SUCCESS('Finished'))
