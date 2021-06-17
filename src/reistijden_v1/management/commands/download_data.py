import datetime
from itertools import islice
from sys import stdout
from time import sleep

from django.core.management.base import BaseCommand
from django.utils import timezone

from reistijden_v1.models import (
    Publication,
    Measurement,
    Location,
    Lane,
    IndividualTravelTime,
    TravelTime,
    MeasuredFlow,
    Category,
)


class Command(BaseCommand):
    help = "Download a subset of the data from acc"

    days = 1

    models = [
        Publication,
        Measurement,
        Location,
        Lane,
        TravelTime,
        IndividualTravelTime,
        MeasuredFlow,
        Category,
    ]

    def add_arguments(self, parser):
        parser.add_argument(
            '--clear-db',
            action='store_true',
            dest='clear_db',
            default=False,
            help='Clear db before downloading',
        )

    def handle(self, *args, **options):
        for model in self.models:
            self.download_table(model=model, clear_db=options['clear_db'])

    def download_table(self, model, batch_size=2500, sleeptime=1, clear_db=False):
        self.stdout.write("\n\n")
        self.stdout.write(self.style.NOTICE("=" * 50))
        self.stdout.write(self.style.NOTICE(f"= Starting {model.__name__} download"))
        self.stdout.write(self.style.NOTICE("=" * 50))

        if clear_db:
            self.stdout.write(
                self.style.SUCCESS(f"Deleting existing {model.__name__}s")
            )
            model.objects.all().delete()

        start_date = timezone.now() - datetime.timedelta(days=self.days + 1)
        end_date = timezone.now() - datetime.timedelta(days=1)

        all_objects = model.objects.using('acc').all()
        if model is Publication:
            all_objects = all_objects.filter(
                measurement_start_time__gte=start_date,
                measurement_start_time__lte=end_date,
            )
        if model is Measurement:
            all_objects = all_objects.filter(
                publication__measurement_start_time__gte=start_date,
                publication__measurement_start_time__lte=end_date,
            )
        elif model in [Location, TravelTime, IndividualTravelTime, MeasuredFlow]:
            all_objects = all_objects.filter(
                measurement__publication__measurement_start_time__gte=start_date,
                measurement__publication__measurement_start_time__lte=end_date,
            )
        elif model is Lane:
            all_objects = all_objects.filter(
                location__measurement__publication__measurement_start_time__gte=start_date,
                location__measurement__publication__measurement_start_time__lte=end_date,
            )
        elif model is Category:
            all_objects = all_objects.filter(
                measured_flow__measurement__publication__measurement_start_time__gte=start_date,
                measured_flow__measurement__publication__measurement_start_time__lte=end_date,
            )

        num_objects = all_objects.count()
        self.stdout.write(
            self.style.NOTICE(f"Number of {model.__name__}s: {num_objects}")
        )

        start = timezone.now()

        objs = all_objects.iterator()
        num_objs = 0
        while True:
            batch = list(islice(objs, batch_size))
            num_objs += batch_size
            if not batch:
                break

            try:
                model.objects.bulk_create(batch, batch_size)
            except Exception as e:
                self.stdout.write(self.style.ERROR(f"Error bulk creating: {e}"))
                continue

            if num_objs % (batch_size * 40) == 0:
                progress = num_objs / num_objects * 100.0
                runtime = timezone.now() - start

                seconds_per_object = runtime.total_seconds() / num_objs
                expected_seconds = seconds_per_object * num_objects
                expected_runtime = datetime.timedelta(seconds=expected_seconds)

                status_msg = (
                    f"[{str(runtime)[:7]} / {str(expected_runtime)[:7]}] "
                    f"{num_objs} objects "
                    f"({progress:.1f}%)"
                )

                self.stdout.write(self.style.SUCCESS(status_msg))
                sleep(sleeptime)

        num_local_objects = model.objects.count()
        self.stdout.write(
            self.style.SUCCESS(f"Downloaded {num_local_objects} {model.__name__}s")
        )
