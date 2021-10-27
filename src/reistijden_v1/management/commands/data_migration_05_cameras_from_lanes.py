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
        SELECT DISTINCT ON (
            measurement_location_id,
            specific_lane,
            camera_id,
            latitude,
            longitude,
            lane_number,
            status,
            view_direction
        )
            camera_id,
            latitude,
            longitude,
            lane.id,
            lane_number,
            status,
            view_direction
        FROM reistijden_v1_lane as lane
    """

    DELETE_QUERY = """
        DELETE FROM reistijden_v1_lane
        WHERE id NOT in (SELECT lane_id FROM reistijden_v1_camera)
    """
