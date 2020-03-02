from django.conf.urls import url

from .views import MetricsView

urlpatterns = [
    url(r"metrics$", MetricsView, name="metrics")
]
