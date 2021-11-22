from rest_framework.views import APIView  # pip install django-rest-framework
from django.http import (
    JsonResponse,
    HttpResponse,
    HttpResponseBadRequest,
    HttpResponseNotFound,
    HttpResponseForbidden,
)
import logging
from geoserver_api.hki_geoserver.korttelialue import Korttelialue

log = logging.getLogger(__name__)


class API(APIView):
    def get(self, request, korttelinnumero=None):
        if not korttelinnumero:
            return HttpResponseBadRequest("Need korttelinnumero!")

        if not request.auth:
            return HttpResponse(status=401)
        geoserver_creds = request.auth.access_geoserver
        if not geoserver_creds:
            return HttpResponseForbidden("No access!")

        # Confirmed access to GeoServer.
        # Go get the data!
        ka = Korttelialue(
            username=geoserver_creds.username, password=geoserver_creds.credential
        )
        ka_data = ka.get(korttelinnumero)
        if not ka_data:
            log.error("%s not found!" % korttelinnumero)
            return HttpResponseNotFound()

        log.debug("Korttelinnumero: %s" % (ka_data["korttelinnumero"]))
        ka_data["geom"] = ka.get_geometry(ka_data)

        return JsonResponse(ka_data)
