import json
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt

from .models import VlogRecord


@csrf_exempt
def post_endpoint(request):
    if request.method != 'POST':
        return HttpResponse(status=405)

    vlog_objects = []
    for line in request.body.decode("utf-8").split("\n"):
        raw = line.strip()
        if raw:
            vlog_objects.append(VlogRecord(raw=raw))
    VlogRecord.objects.bulk_create(vlog_objects)

    return HttpResponse(json.dumps({"created": len(vlog_objects)}), status=201)
