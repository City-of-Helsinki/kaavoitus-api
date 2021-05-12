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
    def get(self, request, hankenumero=None):
        if not hankenumero:
            return HttpResponseBadRequest("Need hankenumero!")

        if not request.auth:
            return HttpResponse(status=401)
        geoserver_creds = request.auth.access_geoserver
        if not geoserver_creds:
            return HttpResponseForbidden("No access!")

        # Confirmed access to GeoServer.
        # Go get the data!
        kh = hki_geoserver.Kaavahanke(
            username=geoserver_creds.username, password=geoserver_creds.credential
        )
        kh_data = kh.get_by_hankenumero(hankenumero)
        if not kh_data:
            log.error("Kaavahanke (%s) not found!" % hankenumero)
            return HttpResponseNotFound()

        log.debug("Hankenumero: %s" % (kh_data["hankenumero"]))
        kh_data["geom"] = kh.get_geometry(kh_data)

        return JsonResponse(kh_data)
