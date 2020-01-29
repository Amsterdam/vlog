from django.db import models
from django.utils import timezone
from django_extensions.db.models import TimeStampedModel

from contrib.timescale.fields import TimescaleDateTimeField


class VlogRecord(TimeStampedModel):
    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['vri_id', 'time'], name='vri_time')
        ]

    time = TimescaleDateTimeField(interval="1 week", default=timezone.now)

    # VRI stands for VerkeersRegelInstallatie. One VRI contains all
    # the installations in one intersection.
    vri_id = models.IntegerField()

    # Max 255 types can exist
    message_type = models.PositiveSmallIntegerField()

    # The message itself.
    message = models.CharField(max_length=255)
