import json
import logging

from django.core.management import BaseCommand
from django.db import connection
from ingress.models import FailedMessage, Message

from reistijden_v1.models import Measurement, Measurement2, MeasurementSite, Publication

logger = logging.getLogger(__name__)


class Command(BaseCommand):
    def handle(self, *args, **options):

        publication_timestamp = None
        if publication := Publication.objects.last():
            publication_timestamp = publication.measurement_start_time

        last_measurement2 = Measurement2.objects.latest('id')

        print(
            json.dumps(
                {
                    'message_count': Message.objects.count(),
                    'failed_message_count': FailedMessage.objects.count(),
                    'measurement_site_count': MeasurementSite.objects.count(),
                    'last_publication_timestamp': publication_timestamp,
                    'measurements': (
                        Measurement.objects.earliest('id').id,
                        Measurement.objects.latest('id').id,
                    ),
                    'measurement2': (
                        Measurement2.objects.earliest('id').id,
                        last_measurement2.id,
                    ),
                    'measurement2_next_batch': (
                        Measurement.objects.filter(
                            id__range=(
                                last_measurement2.id + 1,
                                last_measurement2.id + 10_001,
                            )
                        ).count()
                    ),
                    'first_measurement_after_last_measurement2': (
                        Measurement.objects.filter(id__gt=last_measurement2.id)
                        .earliest('id')
                        .id
                    ),
                },
                indent=2,
                default=str,
            )
        )
