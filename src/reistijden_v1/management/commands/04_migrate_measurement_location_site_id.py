import logging
from math import ceil

from django.db import connection
from django.db.models import F

from reistijden_v1.management.commands.base_command import MyCommand
from reistijden_v1.models import Measurement, MeasurementLocation

logger = logging.getLogger(__name__)


class Command(MyCommand):
    def add_arguments(self, parser):
        parser.add_argument('--sleep', nargs='?', default=1, type=int)

    def handle(self, **options):
        logger.info("message")

        locations = MeasurementLocation.objects.filter(measurement_site=None).exclude(
            measurement=None
        )

        num_locations = locations.count()
        self.success(
            f"Found {num_locations} measurement locations. "
            f"Migrating their measurement sites..."
        )

        max_location_id = MeasurementLocation.objects.order_by('id').last().id

        for i in range(1, 100 + 1):
            max_id = ceil(max_location_id / 100 * i)
            self.notice(f"- Updating locations with ID < {max_id}")
            query = f"""
                UPDATE {MeasurementLocation.objects.model._meta.db_table} AS location
                SET measurement_site_id = measurement.measurement_site_id
                FROM {Measurement.objects.model._meta.db_table} AS measurement
                WHERE location.measurement_id = measurement.id
                AND measurement.measurement_site_id IS NOT NULL
                AND location.measurement_site_id IS NULL
                AND location.id <= %s
            """
            with connection.cursor() as cursor:
                cursor.execute(query, [max_id])

        num_locations = MeasurementLocation.objects.exclude(
            measurement=None, measurement_site=None
        ).count()
        self.success(f"FINISHED! Migrated {num_locations} measurement locations")

        self.validate_results()

    def validate_results(self):
        self.notice("Validating results")
        num_objects = MeasurementLocation.objects.count()
        locations = MeasurementLocation.objects.exclude(
            measurement_site_id=F('measurement__measurement_site_id'),
        )

        # somehow length=None and measurement_site__length=None are seen as diffs
        locations = locations.exclude(
            measurement__measurement_site=None, measurement_site=None
        )

        num_errors = locations.count()
        if num_errors > 0:
            self.stdout.write(
                self.style.ERROR(
                    f"ERROR! Found {num_errors} MeasurementLocation objects "
                    f"(out of {num_objects}) where measurement_site != "
                    f"measurement.measurement_site."
                )
            )
        else:
            self.stdout.write(
                self.style.SUCCESS(
                    f"SUCCESS! All MeasurementLocation objects ({num_objects}) "
                    f"have a correct measurement site"
                )
            )
