from collections import defaultdict, namedtuple
from itertools import groupby
from typing import List

from django.core.management.base import BaseCommand
from django.db import connection

from reistijden_v1.management.commands.util import (
    profile_it,
    sort_and_group_by,
    time_it,
)
from reistijden_v1.models import MeasurementSite


@time_it('get_first_unprocessed_id')
def get_first_unprocessed_id():
    with connection.cursor() as cursor:
        cursor.execute(
            "select min(id) from reistijden_v1_measurement where measurement_site_id is null"
        )
        return cursor.fetchone()[0]


SELECT_DATA_QUERY = """
    select      measurement.id as measurement_id,
                measurement.reference_id,
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
    from        reistijden_v1_measurement as measurement
    left join   reistijden_v1_measurementlocation location on measurement.id = location.measurement_id
    left join   reistijden_v1_lane lane on location.id = lane.measurement_location_id
    and         measurement.measurement_site_id is null
    where       measurement.id between %(first_id)s and %(last_id)s
    order by    measurement_id,
                index,
                specific_lane,
                camera_id,
                latitude,
                longitude,
                lane_number,
                status,
                view_direction
"""


MeasurementSiteKeyRow = namedtuple(
    'MeasurementSiteKeyRow',
    (
        'reference_id',
        'version',
        'name',
        'type',
        'length',
        'index',
        'specific_lane',
        'camera_id',
        'latitude',
        'longitude',
        'lane_number',
        'status',
        'view_direction',
    ),
)


def get_measurement_site_json(data: List[MeasurementSiteKeyRow]):
    """
    Given a measurement site key (tuple of tuples containing the
    data related to a particular measurement site) generate json
    which can be used as a key for selecting in the database.
    """
    measurement_site_json = {
        'reference_id': data[0].reference_id,
        'version': data[0].version,
        'name': data[0].name,
        'type': data[0].type,
        'length': data[0].length,
        'measurement_locations': [],
    }

    # locations are either all NULL, or all not-NULL so we can safely
    # coalesce null values to -1 to allow for sorting, however python
    # cannot handle None < None, so we use -1 as a sentinel value to
    # mean NULL
    for location_index, lanes in sort_and_group_by(
        data,
        lambda x: x.index or -1,
    ):
        location_json = {
            'index': None if location_index == -1 else location_index,
            'lanes': [],
        }
        measurement_site_json['measurement_locations'].append(location_json)

        for specific_lane, cameras in sort_and_group_by(
            lanes,
            lambda x: x.specific_lane,
        ):

            if specific_lane is not None:

                lane_json = {'specific_lane': specific_lane, 'cameras': []}
                location_json['lanes'].append(lane_json)

                for camera in cameras:
                    camera_json = {
                        'camera_id': camera.camera_id,
                        'latitude': float(camera.latitude),
                        'longitude': float(camera.longitude),
                        'lane_number': camera.lane_number,
                        'status': camera.status,
                        'view_direction': camera.view_direction,
                    }
                    lane_json['cameras'].append(camera_json)

    return measurement_site_json


class Command(BaseCommand):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.measurement_site_cache = {}

    @time_it('process_batch')
    def process_batch(self, first_id, batch_size):

        measurement_site_measurements = defaultdict(list)
        created_measurement_sites = 0

        with connection.cursor() as cursor:

            # Get the measurement, location and lanes data for this batch
            last_id = first_id + batch_size
            cursor.execute(SELECT_DATA_QUERY, locals())

            for measurement_id, measurement_rows in groupby(
                cursor.fetchall(),
                key=lambda x: x[0],
            ):
                # exclude the measurement_id from the key
                key = tuple(x[1:] for x in measurement_rows)

                # this is an unknown measurement site, but it might already exist it
                # the database...
                measurement_site = self.measurement_site_cache.get(key)
                if measurement_site is None:

                    # convert the tuple of tuples into something more usable, and
                    # then get the json which represents this measurement_site
                    data = [MeasurementSiteKeyRow(*row) for row in key]
                    measurement_site_json = get_measurement_site_json(data)

                    measurement_site, created = MeasurementSite.objects.get_or_create(
                        reference_id=measurement_site_json['reference_id'],
                        version=measurement_site_json['version'],
                        name=measurement_site_json['name'],
                        type=measurement_site_json['type'],
                        length=measurement_site_json['length'],
                        measurement_site_json=measurement_site_json,
                    )

                    created_measurement_sites += created

                # collect the measurements which relate to this measurement site
                measurement_site_measurements[measurement_site.id].append(
                    measurement_id
                )
                self.measurement_site_cache[key] = measurement_site

            # update all measurements with the appropriate measurement site id
            values = ','.join(
                f'({measurement_site_id}, {measurement_id})'
                for measurement_site_id, measurement_ids in measurement_site_measurements.items()
                for measurement_id in measurement_ids
            )
            cursor.execute(
                f"""
                update reistijden_v1_measurement
                set measurement_site_id=t.measurement_site_id
                from (values {values}) AS t (measurement_site_id, measurement_id)
                where id=measurement_id;
            """
            )

        if created_measurement_sites:
            print(f'Created {created_measurement_sites} measurement sites')

    def add_arguments(self, parser):
        parser.add_argument('batch_size', type=int)
        parser.add_argument('--single', action='store_true')

    @profile_it()
    @time_it('handle')
    def handle(self, *args, **options):

        while True:

            if (first_id := get_first_unprocessed_id()) is None:
                break

            self.process_batch(first_id, options['batch_size'])

            if options['single']:
                break
