import factory

from vlog.models import Vlog


class VlogFactory(factory.Factory):
    class Meta:
        model = Vlog
