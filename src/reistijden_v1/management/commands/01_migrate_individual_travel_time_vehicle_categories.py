import logging

from django.db.models import F

from reistijden_v1.management.commands.base_command import MyCommand
from reistijden_v1.models import IndividualTravelTime, VehicleCategory

logger = logging.getLogger(__name__)


class Command(MyCommand):
    def add_arguments(self, parser):
        parser.add_argument('--sleep', nargs='?', default=1, type=int)

    def handle(self, **options):
        logger.info("message")

        # this query takes a bit less than 2 minutes on acc. Seems acceptable
        unique_categories = (
            IndividualTravelTime.objects.all()
            .values_list('old_vehicle_category', flat=True)
            .distinct()
        )

        num_categories = unique_categories.count()
        self.success(f"Found {num_categories} unique categories. Migrating...")

        category_dict = {}

        for category in unique_categories:
            vehicle_category, _ = VehicleCategory.objects.get_or_create(name=category)
            category_dict[category] = vehicle_category.id

        for category, vehicle_category_id in category_dict.items():
            self.notice(f"- Migrating {category}...")
            IndividualTravelTime.objects.filter(
                vehicle_category_id=None, old_vehicle_category=category
            ).update(vehicle_category_id=vehicle_category_id)

        num_categories = VehicleCategory.objects.count()
        self.success(f"FINISHED! Migrated {num_categories} categories")

        self.validate_results(num_objects=num_categories)

    def validate_results(self, num_objects):
        self.notice("Validating results")
        num_errors = IndividualTravelTime.objects.exclude(
            old_vehicle_category=F('vehicle_category__name')
        ).count()

        if num_errors > 0:
            self.error(
                f"ERROR! Found {num_errors} IndividualTravelTime objects "
                f"(out of {num_objects}) where category is wrong."
            )
        else:
            self.success(
                f"SUCCESS! All IndividualTravelTime objects ({num_objects}) "
                f"have a correct category."
            )
