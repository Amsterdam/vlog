import os

from django.apps import AppConfig


class PrometheusConfig(AppConfig):
    name = 'contrib.prometheus'
    verbose_name = 'Prometheus metrics exporter'

    def ready(self):
        prometheus_dir = os.getenv("prometheus_multiproc_dir")
        if prometheus_dir and not os.path.exists(prometheus_dir):
            os.makedirs(prometheus_dir)
