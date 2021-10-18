import logging

from src.reistijden_v1.management.commands.data_migration_command import (
    DataMigrationCommand,
)

logger = logging.getLogger(__name__)


class Command(DataMigrationCommand):

    UPDATE_QUERY = """
        UPDATE reistijden_v1_measurementlocation AS location
        SET measurement_site_id = measurement.measurement_site_id
        FROM reistijden_v1_measurement AS measurement
        WHERE location.measurement_id = measurement.id
        AND measurement.measurement_site_id IS NOT NULL
    """

    VALIDATE_QUERY = """
        SELECT COUNT(*) as expected,
               COUNT(*) FILTER (
                    WHERE measurement.measurement_site_id != location.measurement_site_id
                    OR measurement.measurement_site_id IS NOT NULL AND location.measurement_site_id IS NULL
                    OR measurement.measurement_site_id IS NULL AND location.measurement_site_id IS NOT NULL
               ) as errors
        FROM reistijden_v1_measurementlocation AS location
        LEFT JOIN reistijden_v1_measurement AS measurement 
            ON location.measurement_id = measurement.id 
    """
