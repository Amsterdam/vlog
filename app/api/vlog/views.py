from django.conf import settings
from rest_framework import exceptions, mixins, status, viewsets
from rest_framework.request import Request
from rest_framework.response import Response

from vlog.models import Vlog
from vlog.utils import parse_vlog_lines

from .serializers import VlogSerializer


class VlogViewSet(
    mixins.CreateModelMixin, mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin, mixins.DestroyModelMixin, mixins.ListModelMixin,
    viewsets.GenericViewSet
):
    """
    A viewset for viewing and editing user instances.
    """
    """
    A viewset that provides default `create()`, `retrieve()`, `update()`,
    `partial_update()`, `destroy()` and `list()` actions.
    """
    serializer_class = VlogSerializer
    queryset = Vlog.objects.all()

    def create(self, request: Request, version):
        # For now we set the vri_id fixed
        vri_id = 101

        # If we receive a string of data we expect it to be
        # a bulk of V-log messages
        data = request.data
        many = False
        if isinstance(data, str):
            data = parse_vlog_lines(data, vri_id=vri_id)
            many = True

            serializer = self.get_serializer(data=data, many=many)
            serializer.is_valid(raise_exception=True)
            self.perform_create(serializer)
            headers = self.get_success_headers(serializer.data)
            return Response(
                serializer.data,
                status=status.HTTP_201_CREATED,
                headers=headers
            )

        return super().create(request)

    def raise_if_not_debug(self):
        if not settings.DEBUG:
            raise exceptions.MethodNotAllowed(self.request.method)

    def list(self, request: Request, version):
        self.raise_if_not_debug()
        return super().list(request)

    def retrieve(self, request: Request, version):
        self.raise_if_not_debug()
        return super().retrieve(request)

    def update(self, request: Request, version):
        self.raise_if_not_debug()
        return super().update(request)

    def partial_update(self, request: Request, version):
        self.raise_if_not_debug()
        return super().list(request)

    def destroy(self, request: Request, version):
        self.raise_if_not_debug()
        return super().list(request)
