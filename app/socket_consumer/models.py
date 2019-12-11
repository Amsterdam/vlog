from django.db import models


class VlogRecord(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)  # The moment this record was written to our database
    recorded_at = models.DateTimeField()  # The moment the record was received by the ESB from the VRI
    vri_id = models.IntegerField()  # VRI stands for VerkeersRegelInstallatie. One VRI contains all the installations
                                    # in one intersection.
    raw = models.CharField(max_length=255)  # The raw record itself.

