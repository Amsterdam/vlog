from django.db import models


class VlogRecord(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    raw = models.CharField(max_length=255)
