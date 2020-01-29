import os
import django
from datetime import datetime
import pytz


os.environ['DJANGO_SETTINGS_MODULE'] = 'settings.settings'
django.setup()

from .models import VlogRecord

timezone = pytz.timezone("Europe/Amsterdam")


def save_line(line):
    values = [x.strip() for x in line.split(',')]
    for value in values:
        if len(value) == 0:
            raise ValueError
    if len(values) != 3:
        raise ValueError

    dt_str, vri_id, raw = values

    dt_obj = timezone.localize(datetime.strptime(dt_str, '%Y-%m-%d %H:%M:%S %f'))

    return VlogRecord.objects.create(recorded_at=dt_obj, vri_id=int(vri_id), raw=raw)
