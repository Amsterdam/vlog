import logging

from reistijden_v1.management.commands.base_command import MyCommand
from reistijden_v1.models import Camera, Lane

logger = logging.getLogger(__name__)


class Command(MyCommand):
    def add_arguments(self, parser):
        parser.add_argument('--sleep', nargs='?', default=1, type=int)

    def handle(self, **options):
        logger.info("message")

        unique_lanes = Lane.objects.distinct(
            'measurement_location__measurement_site',
            'measurement_location__index',
            'specific_lane',
            'camera_id',
            'latitude',
            'longitude',
            'lane_number',
            'status',
            'view_direction',
        ).select_related('measurement_location')

        num_unique_lanes = unique_lanes.count()
        total_lanes = Lane.objects.count()

        self.success(
            f"Found {num_unique_lanes} unique lanes, out of {total_lanes} total"
        )

        for lane in unique_lanes:
            self.notice(f"- Processing lane @ {lane.latitude}, {lane.longitude}...")
            measurement_site = lane.measurement_location.measurement_site
            num_deleted, _ = (
                Lane.objects.filter(
                    measurement_location__measurement_site=measurement_site,
                    measurement_location__index=lane.measurement_location.index,
                    specific_lane=lane.specific_lane,
                    camera_id=lane.camera_id,
                    latitude=lane.latitude,
                    longitude=lane.longitude,
                    lane_number=lane.lane_number,
                    status=lane.status,
                    view_direction=lane.view_direction,
                )
                .exclude(id=lane.id)
                .delete()
            )

            Camera.objects.get_or_create(
                reference_id=lane.camera_id,
                latitude=lane.latitude,
                longitude=lane.longitude,
                lane=lane,
                lane_number=lane.lane_number,
                status=lane.status,
                view_direction=lane.view_direction,
            )

            self.success(f"  Deleted {num_deleted} duplicates.")

        new_total_lanes = Lane.objects.count()
        num_deleted = total_lanes - new_total_lanes
        self.success(f"Deleted a total of {num_deleted} duplicate Lane objects.")
        self.success(f"Created {Camera.objects.count()} new camera's.")
