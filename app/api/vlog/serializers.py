from rest_framework import serializers

from vlog.models import Vlog


class VlogSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vlog
        fields = ['time', 'vri_id', 'message_type', 'message']

    #  message = serializers.CharField(max_length=255)
