from django.core.management.base import BaseCommand

from reistijden_v1.models import (
    Publication,
    Measurement,
    Location,
    Lane,
    TravelTime,
    IndividualTravelTime,
    MeasuredFlow,
    Category,
)


class Command(BaseCommand):
    help = "Print data stats for default db"

    def handle(self, *args, **options):
        for model in [
            Publication,
            Measurement,
            Location,
            Lane,
            TravelTime,
            IndividualTravelTime,
            MeasuredFlow,
            Category,
        ]:
            num_objects = model.objects.count()
            self.stdout.write(f"Num {model.__name__} objects: {num_objects}")
