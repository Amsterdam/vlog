import logging

from django.core.management import BaseCommand

from reistijden_v1.models import Measurement, MeasurementSite

logger = logging.getLogger(__name__)


class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument('--sleep', nargs='?', default=1, type=int)

    def handle(self, **options):
        logger.info("message")

        sleep = options['sleep']

        unique_measurement_sites = Measurement.objects.values_list(
            'measurement_site_reference_id',
            'measurement_site_reference_version',
            'measurement_site_name',
            'measurement_site_type',
            'length'
        ).distinct()

        for measurement_site in unique_measurement_sites:
            measurement_site, _ = MeasurementSite.objects.get_or_create(
                reference_id=measurement_site[0],
                version=measurement_site[1],
                name=measurement_site[2],
                type=measurement_site[3],
                length=measurement_site[4]
            )

            Measurement.objects.filter(
                measurement_site=None,
                measurement_site_reference_id=measurement_site[0],
                measurement_site_reference_version=measurement_site[1],
                measurement_site_name=measurement_site[2],
                measurement_site_type=measurement_site[3],
                length=measurement_site[4],
            ).update(measurement_site=measurement_site)

        self.stdout.write(self.style.SUCCESS('Finished'))
