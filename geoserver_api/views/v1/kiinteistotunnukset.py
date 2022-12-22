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
from api_project.utils import format_kiinteistotunnus

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
            username=geoserver_creds.username,
            password=geoserver_creds.credential,
        )
        data = kh.get_by_hankenumero(hankenumero)

        if not data:
            return HttpResponseNotFound("No data found for hankenumero!")

        kt = hki_geoserver.Kiinteistotunnus(
            username=geoserver_creds.username,
            password=geoserver_creds.credential
        )
        kt_data = kt.get_by_geom(data)

        if not kt_data:
            return HttpResponseNotFound("No kiinteisto data found by geometry")

        kiinteistot = [kt for kiinteisto in kt_data if (kt := format_kiinteistotunnus(kiinteisto["kiinteistotunnus"]))]

        return JsonResponse({"kiinteistotunnukset": kiinteistot})
