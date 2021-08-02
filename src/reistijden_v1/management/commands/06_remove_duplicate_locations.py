import logging

from django.core.management import BaseCommand
from django.db.models import Count

from reistijden_v1.management.commands.base_command import MyCommand
from reistijden_v1.models import Lane, Camera, MeasurementLocation

logger = logging.getLogger(__name__)


class Command(MyCommand):
    def add_arguments(self, parser):
        parser.add_argument('--sleep', nargs='?', default=1, type=int)

    def handle(self, **options):
        logger.info("message")

        sleep = options['sleep']

        superfluous_locations = MeasurementLocation.objects.annotate(
            num_lanes=Count('lane')
        ).filter(num_lanes=0)

        num_superfluous_locations = superfluous_locations.count()
        total_locations = MeasurementLocation.objects.count()

        self.success(
            f"Found {num_superfluous_locations} superfluous locations, "
            f"out of {total_locations} measurement locations"
        )

        num_deleted, _ = superfluous_locations.delete()

        self.success(
            f"Deleted a total of {num_deleted} duplicate MeasurementLocation objects"
        )
