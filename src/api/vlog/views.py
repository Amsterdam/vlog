from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response

from vlog.models import Vlog
from vlog.parsers import parse_vlog_lines

from .serializers import VlogSerializer


class VlogViewSet(viewsets.ModelViewSet):
    """
    A viewset for handling VRI V-log's
    """

    serializer_class = VlogSerializer
    queryset = Vlog.objects.all()
    permission_classes = [IsAuthenticated]

    def create(self, request: Request, **kwargs):
        # If we receive a string of data we expect it to be
        # a bulk of V-log messages
        data = request.data
        many = False
        if isinstance(data, bytes):
            data = parse_vlog_lines(data.decode())
            many = True

            serializer = self.get_serializer(data=data, many=many)
            serializer.is_valid(raise_exception=True)
            self.perform_create(serializer)
            headers = self.get_success_headers(serializer.data)
            return Response("", status=status.HTTP_201_CREATED, headers=headers,)

        return super().create(request)

    @action(methods=["GET"], detail=False)
    def env(self, request: Request, **kwargs):
        """
        Export method, has no pagination and will dump the complete collection.
        """
        headers = {
            x: request.META.get(x) for x in request.META if x.startswith("HTTP_")
        }
        return Response(
            dict(
                version=kwargs.get("version"),
                format=kwargs.get("format"),
                headers=headers,
            )
        )
