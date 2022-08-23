import json
import logging

from django.core.management import BaseCommand
from django.db import connection
from ingress.models import FailedMessage, Message

from reistijden_v1.models import (
    Camera,
    Lane2,
    Measurement,
    Measurement2,
    MeasurementLocation2,
    MeasurementSite,
    Publication,
)

logger = logging.getLogger(__name__)


class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument('--with-measurement-counts', action='store_true')

    def handle(self, *args, **options):

        publication_timestamp = None
        if publication := Publication.objects.last():
            publication_timestamp = publication.measurement_start_time

        if options['with_measurement_counts']:
            measurement_counts = {
                'measurement_count': Measurement.objects.count(),
                'measurement2_count': Measurement2.objects.count(),
            }
        else:
            measurement_counts = {}

        print(
            json.dumps(
                {
                    'message_count': Message.objects.count(),
                    'failed_message_count': FailedMessage.objects.count(),
                    'measurement_site_count': MeasurementSite.objects.count(),
                    'measurement_location_count': MeasurementLocation2.objects.count(),
                    'lane_count': Lane2.objects.count(),
                    'camera_count': Camera.objects.count(),
                    'last_publication_timestamp': publication_timestamp,
                    'measurements': (
                        Measurement.objects.earliest('id').id,
                        Measurement.objects.latest('id').id,
                    ),
                    'measurement2': (
                        Measurement2.objects.earliest('id').id,
                        Measurement2.objects.latest('id').id,
                    ),
                    **measurement_counts,
                },
                indent=2,
                default=str,
            )
        )
