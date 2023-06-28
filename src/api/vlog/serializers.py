from rest_framework import serializers

from vlog.models import Vlog


class VlogListSerializer(serializers.ListSerializer):
    def create(self, validated_data):
        data = [Vlog(**item) for item in validated_data]
        return Vlog.objects.bulk_create(data)


class VlogSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vlog
        fields = ['time', 'vri_id', 'message_type', 'message']
        list_serializer_class = VlogListSerializer
