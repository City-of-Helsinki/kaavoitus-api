from rest_framework.views import APIView  # pip install django-rest-framework
from django.http import (
    JsonResponse,
    HttpResponse,
    HttpResponseBadRequest,
    HttpResponseNotFound,
    HttpResponseForbidden,
)
import logging
from geoserver_api import hki_geoserver

log = logging.getLogger(__name__)


class API(APIView):
    def get(self, request, kiinteistotunnus=None):
        if not kiinteistotunnus:
            return HttpResponseBadRequest("Need kiinteistotunnus!")

        if not request.auth:
            return HttpResponse(status=401)
        geoserver_creds = request.auth.access_geoserver
        if not geoserver_creds:
            return HttpResponseForbidden("No access!")

        # Confirmed access to GeoServer.
        # Go get the data!
        mr = hki_geoserver.Maarekisterikiinteisto(
            username=geoserver_creds.username, password=geoserver_creds.credential
        )
        mr_data = mr.get(kiinteistotunnus)
        if not mr_data:
            log.error("%s not found!" % kiinteistotunnus)
            return HttpResponseNotFound()

        mr_data["geom"] = mr.get_geometry(mr_data)

        return JsonResponse(mr_data)
