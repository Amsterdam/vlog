from django.core.management import BaseCommand

from reistijden_v1.models import MeasurementSite


class Command(BaseCommand):
    def handle(self, *args, **options):
        for measurement_site_json in MeasurementSite.objects.values_list(
            'measurement_site_json', flat=True
        ):
            # measurement sites will already exist, but use get_or_create
            # (can also be used by the serializer) to ensure that the underlying
            # entities (measurement_locations, lanes and cameras) are also
            # created.
            MeasurementSite.get_or_create(measurement_site_json)
