import logging
from typing import Tuple

from django.core.management import BaseCommand
from django.db import connection

logger = logging.getLogger(__name__)


class DataMigrationCommand(BaseCommand):

    # should be overridden by child commands to perform the migration and select
    # the number of values migrated and the number of errors that were detected.
    INSERT_QUERY: str = NotImplemented
    UPDATE_QUERY: str = NotImplemented
    VALIDATE_QUERY: str = NotImplemented

    def handle(self, **options):
        with connection.cursor() as cursor:
            self.migrate(cursor)
            self.validate(cursor)

    def migrate(self, cursor):
        """
        Peform the actual data migration.

        :param cursor: Cursor to use for executing queries.
        """
        if self.INSERT_QUERY is not NotImplemented:
            logging.info("Inserting")
            cursor.execute(self.INSERT_QUERY)

        logging.info("Updating")
        cursor.execute(self.UPDATE_QUERY)

    def validate(self, cursor) -> Tuple[int, int]:
        """
        Perform a sanity check to validate that the data has been correctly
        migrated.

        Sub-classes should define VALIDATION_QUERY which selects the number
        of expected rows and the number of rows with errors.

        :param cursor: Cursor to use for executing queries.

        :return: Tuple of (expected number of rows, number of rows with errors).
        """
        logger.info("Validating")

        cursor.execute(self.VALIDATE_QUERY)
        num_objects, num_errors = cursor.fetchone()

        if num_errors > 0:
            self.error(
                f"ERROR! Found {num_errors} objects "
                f"(out of {num_objects}) where migrated data is wrong."
            )
        else:
            self.success(
                f"SUCCESS! All objects ({num_objects}) "
                f"have been correctly migrated."
            )

        return num_objects, num_errors

    def success(self, msg):
        self.stdout.write(self.style.SUCCESS(msg))

    def notice(self, msg):
        self.stdout.write(self.style.NOTICE(msg))

    def error(self, msg):
        self.stdout.write(self.style.ERROR(msg))
