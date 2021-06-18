from django.core.management.base import BaseCommand

from reistijden_v1.models import (
    Publication,
    Measurement,
    Lane,
    TravelTime,
    IndividualTravelTime, VehicleCategory, MeasurementSite, MeasurementLocation, Camera,
    TrafficFlow, TrafficFlowCategoryCount,
)


class Command(BaseCommand):
    help = "Print data stats for default db"

    def handle(self, *args, **options):
        for model in [
            Publication,
            Measurement,
            MeasurementSite,
            MeasurementLocation,
            Lane,
            Camera,
            TravelTime,
            IndividualTravelTime,
            TrafficFlow,
            TrafficFlowCategoryCount,
            VehicleCategory,
        ]:
            num_objects = model.objects.count()
            self.stdout.write(f"Num {model.__name__} objects: {num_objects}")
