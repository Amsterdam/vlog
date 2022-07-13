import logging

from reistijden_v1.management.commands.data_migration_command import (
    DataMigrationCommand,
)

logger = logging.getLogger(__name__)


class Command(DataMigrationCommand):
    def migrate(self, cursor):

        # Collect all unique lane and location information, we will clear these tables
        # and fill them again so only unique data remains.
        cursor.execute(
            """
            select distinct
               -- lane
               specific_lane,
               camera_id,
               latitude,
               longitude,
               lane_number,
               status,
               view_direction,
               -- location
               index,
               measurement_site_id
            into temporary table all_locations
            from reistijden_v1_lane
            join reistijden_v1_measurementlocation rv1m on reistijden_v1_lane.measurement_location_id = rv1m.id
        """
        )

        # Delete all lane and location information
        cursor.execute("delete from reistijden_v1_lane")
        cursor.execute("delete from reistijden_v1_measurementlocation")

        # Reinsert all distinct locations (must be distinct since there may be
        # multiple lanes for the same location).
        cursor.execute(
            """
            insert into reistijden_v1_measurementlocation
            (
                index,
                measurement_site_id
            )
            select distinct index,
                   measurement_site_id
            from   all_locations
        """
        )

        # Reinsert all distinct lanes
        cursor.execute(
            """
            insert into reistijden_v1_lane
            (
                specific_lane,
                camera_id,
                latitude,
                longitude,
                lane_number,
                status,
                view_direction,
                measurement_location_id
            )
            select distinct specific_lane,
                   camera_id,
                   latitude,
                   longitude,
                   lane_number,
                   status,
                   view_direction,
                   rv1m.id
            from all_locations
            join reistijden_v1_measurementlocation rv1m on
                all_locations.index = rv1m.index and all_locations.measurement_site_id = rv1m.measurement_site_id
        """
        )
