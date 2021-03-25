from rest_framework import routers

from .vlog.views import VlogViewSet

app_name = 'api'
router = routers.DefaultRouter()
router.register('vlogs', VlogViewSet)
urlpatterns = router.urls
