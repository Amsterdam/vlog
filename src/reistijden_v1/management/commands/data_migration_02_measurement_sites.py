import logging

from src.reistijden_v1.management.commands.data_migration_command import (
    DataMigrationCommand,
)

logger = logging.getLogger(__name__)


class Command(DataMigrationCommand):

    INSERT_QUERY = """
        INSERT INTO reistijden_v1_measurementsite (
            reference_id,
            version,
            name,
            type,
            length
        )
        SELECT DISTINCT
            reference_id,
            version,
            name,
            type,
            length
        FROM reistijden_v1_measurement
    """

    UPDATE_QUERY = """
        UPDATE reistijden_v1_measurement as m
        SET measurement_site_id=ms.id
        FROM reistijden_v1_measurementsite as ms
        WHERE
            m.reference_id=ms.reference_id AND
            m.version=ms.version AND
            m.name=ms.name AND
            m.type=ms.type AND
            (m.length=ms.length OR coalesce(m.length, ms.length) is null)
    """

    VALIDATE_QUERY = """
        SELECT COUNT(*) as expected,
               COUNT(*) FILTER (WHERE ms.id IS NULL) as errors
        FROM reistijden_v1_measurement AS m
        LEFT JOIN reistijden_v1_measurementsite AS ms ON
                m.reference_id=ms.reference_id AND
                m.version=ms.version AND
                m.name=ms.name AND
                m.type=ms.type AND
                (m.length=ms.length OR coalesce(m.length, ms.length) is null)
    """
