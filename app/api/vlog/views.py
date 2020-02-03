from rest_framework import status, viewsets
from rest_framework.request import Request
from rest_framework.response import Response

from vlog.models import Vlog
from vlog.utils import parse_vlog_lines

from .serializers import VlogSerializer


class VlogViewSet(viewsets.ModelViewSet):
    """
    A viewset for viewing and editing user instances.
    """
    serializer_class = VlogSerializer
    queryset = Vlog.objects.all()

    def list(self, request: Request, version):
        return Response(dict(
            version=version,
            params=request.query_params,
        ))

    def create(self, request: Request, version):
        vri_id = 101
        data = request.data
        many = False
        if isinstance(data, str):
            data = parse_vlog_lines(request.data, vri_id=vri_id)
            many = True

        serializer = self.get_serializer(data=data, many=many)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(
            serializer.data, status=status.HTTP_201_CREATED, headers=headers
        )
