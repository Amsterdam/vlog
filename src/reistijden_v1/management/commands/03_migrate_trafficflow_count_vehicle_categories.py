import logging

from django.db.models import F, Q

from reistijden_v1.management.commands.base_command import MyCommand
from reistijden_v1.models import (
    VehicleCategory,
    TrafficFlowCategoryCount,
)

logger = logging.getLogger(__name__)


class Command(MyCommand):
    def add_arguments(self, parser):
        parser.add_argument('--sleep', nargs='?', default=1, type=int)

    def handle(self, **options):
        logger.info("message")

        sleep = options['sleep']

        unique_categories = TrafficFlowCategoryCount.objects.exclude(
            type=None
        ).distinct('type')

        num_categories = unique_categories.count()
        self.success(
            f"Found {num_categories} unique Traffic flow categories. Migrating..."
        )

        for category in unique_categories:
            self.notice(f"- Migrating {category.type}...")
            vehicle_category, _ = VehicleCategory.objects.get_or_create(
                name=category.type
            )

            TrafficFlowCategoryCount.objects.filter(
                vehicle_category=None,
                type=category.type,
            ).update(vehicle_category_id=vehicle_category.id)

        num_categories = VehicleCategory.objects.count()
        self.success(f"FINISHED! Migrated {num_categories} categories")

        self.validate_results()

    def validate_results(self):
        self.notice("Validating results")
        num_objects = TrafficFlowCategoryCount.objects.count()
        category_counts = TrafficFlowCategoryCount.objects.exclude(
            Q(type=F('vehicle_category__name')) |
            Q(type=None),
        )

        num_errors = category_counts.count()
        if num_errors > 0:
            self.stdout.write(
                self.style.ERROR(
                    f"ERROR! Found {num_errors} TrafficFlowCategoryCount objects "
                    f"(out of {num_objects}) where vehicle category name is different."
                )
            )
        else:
            self.stdout.write(
                self.style.SUCCESS(
                    f"SUCCESS! All TrafficFlowCategoryCount objects ({num_objects}) "
                    f"have a correct vehicle category"
                )
            )
