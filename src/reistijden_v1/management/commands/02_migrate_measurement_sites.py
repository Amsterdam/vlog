import logging

from django.db.models import F

from reistijden_v1.management.commands.base_command import MyCommand
from reistijden_v1.models import Measurement, MeasurementSite

logger = logging.getLogger(__name__)


class Command(MyCommand):
    def add_arguments(self, parser):
        parser.add_argument('--sleep', nargs='?', default=1, type=int)

    def handle(self, **options):
        logger.info("message")

        unique_measurement_sites = Measurement.objects.values_list(
            'measurement_site_reference_id',
            'measurement_site_reference_version',
            'measurement_site_name',
            'measurement_site_type',
            'length',
        ).distinct()

        num_measurement_sites = unique_measurement_sites.count()
        self.success(f"Found {num_measurement_sites} measurement sites. Migrating...")

        for measurement_site in unique_measurement_sites:
            reference_id = measurement_site[0]
            reference_version = measurement_site[1]
            name = measurement_site[2]
            type = measurement_site[3]
            length = measurement_site[4]

            self.notice(f"- Migrating {name}...")
            measurement_site, _ = MeasurementSite.objects.get_or_create(
                reference_id=reference_id,
                version=reference_version,
                name=name,
                type=type,
                length=length,
            )

            Measurement.objects.filter(
                measurement_site=None,
                measurement_site_reference_id=reference_id,
                measurement_site_reference_version=reference_version,
                measurement_site_name=name,
                measurement_site_type=type,
                length=length,
            ).update(measurement_site=measurement_site)

        num_measurement_sites = MeasurementSite.objects.count()
        self.success(f"FINISHED! Migrated {num_measurement_sites} measurement sites")

        self.validate_results()

    def validate_results(self):
        self.notice("Validating results")
        num_objects = Measurement.objects.count()
        measurements = Measurement.objects.exclude(
            measurement_site_reference_id=F('measurement_site__reference_id'),
            measurement_site_reference_version=F('measurement_site__version'),
            measurement_site_name=F('measurement_site__name'),
            measurement_site_type=F('measurement_site__type'),
            length=F('measurement_site__length'),
        )

        # somehow length=None and measurement_site__length=None are seen as diffs
        measurements = measurements.exclude(length=None, measurement_site__length=None)

        num_errors = measurements.count()
        if num_errors > 0:
            self.stdout.write(
                self.style.ERROR(
                    f"ERROR! Found {num_errors} Measurement objects "
                    f"(out of {num_objects}) where measurement site info is different."
                )
            )
        else:
            self.stdout.write(
                self.style.SUCCESS(
                    f"SUCCESS! All Measurement objects ({num_objects}) "
                    f"have a correct measurement site"
                )
            )
