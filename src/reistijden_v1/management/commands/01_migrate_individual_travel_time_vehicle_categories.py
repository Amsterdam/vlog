import logging

from django.core.management import BaseCommand

from reistijden_v1.models import IndividualTravelTime, VehicleCategory

logger = logging.getLogger(__name__)


class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument('--sleep', nargs='?', default=1, type=int)

    def handle(self, **options):
        logger.info("message")

        sleep = options['sleep']

        # this query takes a bit less than 2 minutes on acc. Seems acceptable
        unique_categories = (
            IndividualTravelTime.objects.all()
            .values_list('old_vehicle_category', flat=True)
            .distinct()
        )

        category_dict = {}

        for category in unique_categories:
            vehicle_category, _ = VehicleCategory.objects.get_or_create(name=category)
            category_dict[category] = vehicle_category.id

        for category, vehicle_category_id in category_dict.items():
            IndividualTravelTime.objects.filter(
                vehicle_category_id=None, old_vehicle_category=category
            ).update(vehicle_category_id=vehicle_category_id)

        self.stdout.write(self.style.SUCCESS('Finished'))
