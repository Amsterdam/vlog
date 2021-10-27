import logging

from reistijden_v1.management.commands.data_migration_command import (
    DataMigrationCommand,
)

logger = logging.getLogger(__name__)


class Command(DataMigrationCommand):

    DELETE_QUERY = """
        DELETE FROM reistijden_v1_measurementlocation
        WHERE id NOT in (SELECT measurement_location_id FROM reistijden_v1_lane)
    """
