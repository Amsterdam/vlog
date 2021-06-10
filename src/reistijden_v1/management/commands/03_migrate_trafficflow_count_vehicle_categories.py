import logging

from django.core.management import BaseCommand

from reistijden_v1.models import (
    IndividualTravelTime,
    VehicleCategory,
    TrafficFlowCategoryCount,
)

logger = logging.getLogger(__name__)


class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument('--sleep', nargs='?', default=1, type=int)

    def handle(self, **options):
        logger.info("message")

        sleep = options['sleep']

        unique_categories = (
            TrafficFlowCategoryCount.objects.all()
            .values_list('type', flat=True)
            .distinct()
        )

        category_dict = {vc.name: vc.id for vc in VehicleCategory.objects.all()}

        for category in unique_categories:
            if category not in category_dict:
                vehicle_category = VehicleCategory.objects.create(name=category)
                category_dict[category] = vehicle_category.id

        for category, vehicle_category_id in category_dict.items():
            TrafficFlowCategoryCount.objects.filter(type=category).update(
                vehicle_category_id=vehicle_category_id
            )

        self.stdout.write(self.style.SUCCESS('Finished'))
