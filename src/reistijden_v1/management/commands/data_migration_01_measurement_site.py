import sys
from decimal import Decimal
from itertools import groupby
from typing import List, NamedTuple

from django.core.management.base import BaseCommand
from django.db import connection

from reistijden_v1.management.commands.util import (
    profile_it,
    sort_and_group_by,
    time_it,
)
from reistijden_v1.models import MeasurementSite


class MeasurementSiteKeyRow(NamedTuple):
    reference_id: str
    version: str
    name: str
    type: str
    length: str
    index: str
    specific_lane: str
    camera_id: str
    latitude: str
    longitude: str
    lane_number: str
    status: str
    view_direction: str


def get_measurement_site_json(data: List[MeasurementSiteKeyRow]):
    """
    Given data about a measurement site (measurement site meta data,
    list of locations and lanes) generate json which can be used
    as a key for selecting in the database. We only need to worry
    about the ordering of lists since postgres will use JSONB type
    and the order of keys are normalized, e.g.

    {'a': 1, 'b': 2} == {'b': 1, 'a': 2}

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
            # convert -1 back to NULL
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
                        'reference_id': camera.camera_id,
                        'latitude': str(camera.latitude),
                        'longitude': str(camera.longitude),
                        'lane_number': camera.lane_number,
                        'status': camera.status,
                        'view_direction': camera.view_direction,
                    }
                    lane_json['cameras'].append(camera_json)

    return measurement_site_json


class Command(BaseCommand):
    """
    Command which will create new Measurement2 and MeasurementSite rows based
    on existing Measurement, MeasurementLocation and Lane data. This old model
    is not denormalized, meaning the measurement site meta data (contained in
    Measurement), locations and lanes are duplicated for each measurement
    (currently at around 600M rows). This data migration is part of a larger
    migration to normalize and deduplicate this model, so that each measurement
    site is only stored once, and referenced by the various measurements.
    A measurement site looks something like...

        reference: Wibautstraat
        ...
        locations:
            - index: 1,
              lanes:
                - specific_index: 'lane1'
                  cameras: {...}

    However it is important to note that measurements are linked to MeasurementSite
    meaning that if anything changes in the underlying configuration an entirely
    new measurement site must be created, otherwise it is not possible to link
    historical records with the configuration at the time the publication was made.

    The strategy applied here is to process the table in a loop with each loop
    processing a large batch (e.g. 10000 rows per batch). So that if the process fails
    we can just restart the process and continue from the previously processed record.

    After some experimentation it seems that updating existing tables causes so much
    junk to be created that the actual query which performs the migration becomes
    slow. This could be solved with a VACUUM FULL ANALYSE, but given the size of the
    table this makes the migration even slower. Therefore, we insert into a new
    measurement table, once the migration is complete we can remove the old table.
    Since we are only storing the id, publication_id and measurent_site_id the
    overhead of this extra table is acceptable, particularly since updating the
    existing table will also be inefficient in terms of space until the vacuum is
    run.
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.measurement_site_cache = {}

    @time_it('process_batch')
    def process_batch(self, cursor, next_id, batch_size, profiler):

        # Get the measurement, location and lanes data for this batch
        SELECT_DATA_QUERY = """
            select      measurement.id as measurement_id,
                        measurement.publication_id as publication_id,
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
            from        reistijden_v1_measurementold as measurement
            left join   reistijden_v1_measurementlocationold location on measurement.id = location.measurement_id
            left join   reistijden_v1_laneold lane on location.id = lane.measurement_location_id
            where       measurement.id between %(next_id)s and (%(next_id)s + %(batch_size)s)
            order by    measurement_id, location.id, lane.id
        """
        cursor.execute(SELECT_DATA_QUERY, locals())

        measurement_id = -1
        created_measurement_sites = 0

        # collect the values to use in the insert statement for measurements
        # and their associated publication id, and measurement site id
        values = []

        # group the data so that for each measurement we have a list of the
        # associated locations and lanes, convert this (already sorted in
        # SQL) list to a tuple which is used to determine if we already saw
        # this measurement site or not. Keeping a local cache like this means
        # we can reduce the amount of work that needs to be done between runs
        # (measurement sites are rarely added)
        for (measurement_id, publication_id), measurement_rows in groupby(
            cursor.fetchall(),
            key=lambda x: x[:2],
        ):
            # exclude the measurement_id and publication_id from the key
            key = tuple(x[2:] for x in measurement_rows)

            # this is an unknown measurement site, but it might already exist it
            # the database...
            if (measurement_site := self.measurement_site_cache.get(key)) is None:

                # This section of code should run very rarely, as such we are
                # not interested in profiling here, the most bang for the buck
                # optimisations should happen outside of this logic branch. which
                # Compared to the rest of the loop we expect this to run at most
                # a few thousand times, compared to hundreds of millions of times
                # for the rest of the loop.
                profiler.stop()

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
                self.measurement_site_cache[key] = measurement_site

                profiler.start()

            # collect the measurements which relate to this measurement site
            values.append(f'({measurement_id},{publication_id},{measurement_site.id})')

        # insert all measurements with the appropriate measurement site id
        if values:
            cursor.execute(
                "insert into reistijden_v1_measurement "
                "(id, publication_id, measurement_site_id) values " + ",".join(values)
            )

        if created_measurement_sites:
            print(f'Created {created_measurement_sites} measurement sites')

        if measurement_id != -1:
            cursor.execute(
                f"SELECT setval('reistijden_v1_measurement2_id_seq', {measurement_id})"
            )

        return measurement_id + 1

    def add_arguments(self, parser):
        parser.add_argument('--batch-size', type=int, default=10_000)
        parser.add_argument('--num-batches', type=int, default=sys.maxsize)

    @time_it('handle')
    def handle(self, *args, **options):

        with connection.cursor() as cursor:

            with time_it('get first unprocessed id'):
                cursor.execute("select max(id) + 1 from reistijden_v1_measurement")
                next_id = cursor.fetchone()[0] or 1

            with profile_it() as profiler:
                for _ in range(options['num_batches']):
                    if not (
                        next_id := self.process_batch(
                            cursor,
                            next_id,
                            options['batch_size'],
                            profiler,
                        )
                    ):
                        # no more batches to process
                        break
