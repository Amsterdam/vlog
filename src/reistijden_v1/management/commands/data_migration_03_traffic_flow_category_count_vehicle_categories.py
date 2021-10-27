import logging

from src.reistijden_v1.management.commands.data_migration_command import (
    DataMigrationCommand,
)

logger = logging.getLogger(__name__)


class Command(DataMigrationCommand):

    INSERT_QUERY = """
        INSERT INTO reistijden_v1_vehiclecategory (name)
        SELECT DISTINCT type
        FROM reistijden_v1_trafficflowcategorycount
        ON CONFLICT DO NOTHING
    """

    UPDATE_QUERY = """
        UPDATE reistijden_v1_trafficflowcategorycount
        SET vehicle_category_id=reistijden_v1_vehiclecategory.id
        FROM reistijden_v1_vehiclecategory
        WHERE type=name
    """

    VALIDATE_QUERY = """
        SELECT COUNT(*) as expected,
               COUNT(*) FILTER (WHERE reistijden_v1_vehiclecategory.id IS NULL) as errors
        FROM reistijden_v1_trafficflowcategorycount
        LEFT JOIN reistijden_v1_vehiclecategory ON type=name
    """  # noqa
