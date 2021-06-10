import logging

from django.core.management import BaseCommand

from reistijden_v1.models import Lane, Camera

logger = logging.getLogger(__name__)


class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument('--sleep', nargs='?', default=1, type=int)

    def handle(self, **options):
        logger.info("message")

        sleep = options['sleep']

        unique_cameras = Lane.objects.values_list(
            'id',
            'camera_id',
            'latitude',
            'longitude',
            'lane_number',
            'status',
            'view_direction'
        ).distinct()

        for camera in unique_cameras:
            Camera.objects.create(
                lane_id=camera[0],
                reference_id=camera[1],
                latitude=camera[2],
                longitude=camera[3],
                lane_number=camera[4],
                status=camera[5],
                view_direction=camera[6]
            )

        self.stdout.write(self.style.SUCCESS('Finished'))
