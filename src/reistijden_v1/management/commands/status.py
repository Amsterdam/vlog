import json
import logging

from django.core.management import BaseCommand
from django.db import connection
from ingress.models import FailedMessage, Message

from reistijden_v1.models import (
    Camera,
    Lane,
    Measurement,
    MeasurementLocation,
    MeasurementOld,
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
                'measurement_old_count': MeasurementOld.objects.count(),
                'measurement_count': Measurement.objects.count(),
            }
        else:
            measurement_counts = {}

        print(
            json.dumps(
                {
                    'message_count': Message.objects.count(),
                    'failed_message_count': FailedMessage.objects.count(),
                    'measurement_site_count': MeasurementSite.objects.count(),
                    'measurement_location_count': MeasurementLocation.objects.count(),
                    'lane_count': Lane.objects.count(),
                    'camera_count': Camera.objects.count(),
                    'last_publication_timestamp': publication_timestamp,
                    'measurements_old': (
                        MeasurementOld.objects.earliest('id').id,
                        MeasurementOld.objects.latest('id').id,
                    ),
                    'measurements': (
                        Measurement.objects.earliest('id').id,
                        Measurement.objects.latest('id').id,
                    ),
                    **measurement_counts,
                },
                indent=2,
                default=str,
            )
        )
