import logging

from src.reistijden_v1.management.commands.data_migration_command import (
    DataMigrationCommand,
)

logger = logging.getLogger(__name__)


class Command(DataMigrationCommand):

    INSERT_QUERY = """
        INSERT INTO reistijden_v1_vehiclecategory (name)
        SELECT DISTINCT old_vehicle_category
        FROM reistijden_v1_individualtraveltime
        WHERE old_vehicle_category IS NOT NULL
    """

    UPDATE_QUERY = """
        UPDATE reistijden_v1_individualtraveltime
        SET vehicle_category_id=reistijden_v1_vehiclecategory.id
        FROM reistijden_v1_vehiclecategory
        WHERE old_vehicle_category=reistijden_v1_vehiclecategory.name
    """

    VALIDATE_QUERY = """
        SELECT COUNT(*) as expected,
               COUNT(*) FILTER (WHERE reistijden_v1_vehiclecategory.id IS NULL) as errors
        FROM reistijden_v1_individualtraveltime
        LEFT JOIN reistijden_v1_vehiclecategory 
                  ON old_vehicle_category=reistijden_v1_vehiclecategory.name
    """
