import itertools
import time

from django.core.management.base import BaseCommand
from django.db import connection

from reistijden_v1.models import MeasurementSite


def group_by(items, key):
    """
    Combine sorted and itertools.groupby since groupby assumes
    that the items to be grouped are also already sorted, which
    may not be the case.
    """
    return itertools.groupby(sorted(items, key=key), key=key)


def fetch_all_dicts(cursor):
    """
    like fetchall, but yields a dict for each row using the cursor
    description for the keys.

    NOTE: Column names must be unique.
    """
    columns = [c[0] for c in cursor.description]
    assert len(set(columns)) == len(cursor.description), "column names must be unique"
    for row in cursor.fetchall():
        yield dict(zip(columns, row))


class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument('batch_size', type=int)

    SELECT_DATA_QUERY = """
        select      measurement.id as measurement_id,
                    measurement.reference_id,
                    measurement.version,
                    measurement.name,
                    measurement.type,
                    measurement.length,
                    location.id as location_id,
                    location.index,
                    lane.id as lane_id,
                    lane.specific_lane,
                    lane.camera_id,
                    lane.latitude,
                    lane.longitude,
                    lane.lane_number,
                    lane.status,
                    lane.view_direction
        from        reistijden_v1_measurement as measurement
        left join   reistijden_v1_measurementlocation location on measurement.id = location.measurement_id
        left join   reistijden_v1_lane lane on location.id = lane.measurement_location_id
        where       measurement.id between %s and %s
        and         measurement.measurement_site_id is null
        order by    measurement.reference_id,
                    measurement.version,
                    measurement.name,
                    measurement.type,
                    measurement.length,
                    location.index,
                    lane.specific_lane,
                    lane.camera_id,
                    lane.latitude,
                    lane.longitude,
                    lane.lane_number,
                    lane.status,
                    lane.view_direction
    """

    SELECT_MIN_ID_QUERY = """
        select min(id)
        from   reistijden_v1_measurement
        where  measurement_site_id is null
    """

    def handle(self, *args, **options):

        batch_size = options['batch_size']
        start_time = time.time()

        with connection.cursor() as cursor:

            # get the id of the first measurement which has not yet been processed
            cursor.execute(self.SELECT_MIN_ID_QUERY)
            first_id = cursor.fetchone()[0]

            # get the data which will be inserted into measurement_site
            cursor.execute(
                self.SELECT_DATA_QUERY,
                [
                    first_id,
                    first_id + batch_size,
                ],
            )

            result = fetch_all_dicts(cursor)

            measurement_sites = []
            for measurement_id, locations in group_by(
                result, lambda x: x['measurement_id']
            ):

                locations = list(locations)
                measurement_site = MeasurementSite(
                    reference_id=locations[0]['reference_id'],
                    version=locations[0]['version'],
                    name=locations[0]['name'],
                    type=locations[0]['type'],
                    length=locations[0]['length'],
                    measurement_site_json={
                        'reference_id': locations[0]['reference_id'],
                        'version': locations[0]['version'],
                        'name': locations[0]['name'],
                        'type': locations[0]['type'],
                        'length': locations[0]['length'],
                        'measurement_locations': [],
                    },
                )
                measurement_sites.append(measurement_site)

                # locations are either all NULL, or all not-NULL so we can safely
                # coalesce null values to -1 to allow for sorting.
                for location_index, lanes in group_by(
                    locations, lambda x: x['index'] or -1
                ):

                    location_json = {
                        'index': location_index,
                        'lanes': [],
                    }
                    measurement_site.measurement_site_json[
                        'measurement_locations'
                    ].append(location_json)

                    for specific_lane, cameras in group_by(
                        lanes, lambda x: x['specific_lane']
                    ):

                        lane_json = {'specific_lane': specific_lane, 'cameras': []}
                        location_json['lanes'].append(lane_json)

                        for camera in cameras:
                            camera_json = {
                                'camera_id': camera['camera_id'],
                                'latitude': None
                                if camera['latitude'] is None
                                else float(camera['latitude']),
                                'longitude': None
                                if camera['longitude'] is None
                                else float(camera['longitude']),
                                'lane_number': camera['lane_number'],
                                'status': camera['status'],
                                'view_direction': camera['view_direction'],
                            }
                            lane_json['cameras'].append(camera_json)

            duration = time.time() - start_time
            self.stdout.write(
                self.style.SUCCESS(
                    f'{len(measurement_sites)} measurement site json blobs created in {duration} seconds'
                )
            )

            # There is a unique constraint on the column measurement_site_json
            # by ignoring conflicts the data will be deduplicated.
            start_time = time.time()
            MeasurementSite.objects.bulk_create(
                measurement_sites, ignore_conflicts=True
            )

            duration = time.time() - start_time
            self.stdout.write(
                self.style.SUCCESS(
                    f'{MeasurementSite.objects.count()} MeasurementSite instances created in {duration} seconds'
                )
            )
