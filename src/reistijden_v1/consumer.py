import logging

from ingress.consumer.base import BaseConsumer
from rest_framework.exceptions import ValidationError

from reistijden_v1.parser import ReistijdenParser
from reistijden_v1.serializers import PublicationSerializer

logger = logging.getLogger(__name__)


class ReistijdenConsumer(BaseConsumer):
    collection_name = 'reistijden_v1'

    def consume_raw_data(self, raw_data):
        # note that exceptions are not handled here, but must be raised
        # so that the message will be moved to the failed queue.
        try:
            restructured_data = ReistijdenParser(raw_data).restructure_data()

            publication_serializer = PublicationSerializer(data=restructured_data)
            publication_serializer.is_valid(raise_exception=True)
            publication_serializer.save()
        except ValidationError as e:
            logger.error('Validation Error on consume_raw_data')
            logger.exception(e)
            self.on_consume_error(raw_data)
        except Exception as e:
            logger.error("Exception called on consume_raw_data")
            logger.exception(e)
            self.on_consume_error(raw_data)
