import logging
from xml.parsers.expat import ExpatError

from rest_framework import exceptions, status, viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework_xml.parsers import XMLParser

from .serializers import PublicationSerializer

logger = logging.getLogger(__name__)


class PublicationViewSet(viewsets.ModelViewSet):
    serializer_class = PublicationSerializer
    serializer_detail_class = PublicationSerializer
    parser_classes = [XMLParser]

    http_method_names = ['post']
    permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):
        try:
            restructured_data = restructure_data(request.body.decode("utf-8"))
        except UnicodeError as e:
            logger.error(e)
            store_error_content(e, request)
            return Response(str(e), status=status.HTTP_400_BAD_REQUEST)
        except (exceptions.ValidationError, KeyError, TypeError) as e:
            logger.error(e)
            store_error_content(e, request)
            return Response(str(e), status=status.HTTP_400_BAD_REQUEST)
        except ExpatError as e:
            logger.error(e)
            store_error_content(e, request)
            return Response(str(e), status=status.HTTP_400_BAD_REQUEST)

        publication_serializer = PublicationSerializer(data=restructured_data)
        publication_serializer.is_valid(raise_exception=True)
        publication_serializer.save()

        return Response("", status=status.HTTP_201_CREATED)
