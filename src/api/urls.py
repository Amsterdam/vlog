from rest_framework import routers

from .reistijden_v1.views import ReistijdenViewSet
from .vlog.views import VlogViewSet

app_name = 'api'
router = routers.DefaultRouter()
router.register('vlogs', VlogViewSet)
router.register('reistijden', ReistijdenViewSet, basename='reistijden')
urlpatterns = router.urls
