import logging

from django.conf import settings
from django.db import connection
from django.http import HttpResponse

log = logging.getLogger(__name__)


def health(request):
    # check debug
    if settings.DEBUG:
        log.exception("Debug mode not allowed in production")
        return HttpResponse(
            "Debug mode not allowed in production",
            content_type="text/plain",
            status=500,
        )

    # check default database
    try:
        with connection.cursor() as cursor:
            cursor.execute("select 1")
            assert cursor.fetchone()
    except Exception as e:
        log.exception(f"Database connectivity failed: {str(e)}")
        return HttpResponse(
            "Database connectivity failed", content_type="text/plain", status=500
        )

    return HttpResponse("Connectivity OK", content_type='text/plain', status=200)
