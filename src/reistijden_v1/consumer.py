import logging

from ingress.consumer.base import BaseConsumer

from reistijden_v1.serializers import PublicationSerializer
from reistijden_v1.parser import ReistijdenParser

logger = logging.getLogger(__name__)


class ReistijdenConsumer(BaseConsumer):
    collection_name = 'reistijden_v1'

    def consume_raw_data(self, raw_data):
        # note that exceptions are not handled here, but must be raised
        # so that the message will be moved to the failed queue.
        restructured_data = ReistijdenParser(raw_data).restructure_data()

        publication_serializer = PublicationSerializer(data=restructured_data)
        publication_serializer.is_valid(raise_exception=True)
        publication_serializer.save()
