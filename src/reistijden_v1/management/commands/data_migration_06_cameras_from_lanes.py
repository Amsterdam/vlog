import logging

from src.reistijden_v1.management.commands.data_migration_command import (
    DataMigrationCommand,
)

logger = logging.getLogger(__name__)


class Command(DataMigrationCommand):

    INSERT_QUERY = """
        INSERT INTO reistijden_v1_camera (
            reference_id,
            latitude,
            longitude,
            lane_id,
            lane_number,
            status,
            view_direction
        )
        SELECT DISTINCT
            camera_id,
            latitude,
            longitude,
            lane.id,
            lane_number,
            status,
            view_direction
        FROM reistijden_v1_lane as lane
    """
