from geoserver_api.hki_geoserver import kiinteistotunnus
from geoserver_api.views.serializers.v1.kiinteistov1serializer import KiinteistoV1Serializer
from rest_framework.views import APIView  # pip install django-rest-framework
from django.http import JsonResponse, HttpResponse, HttpResponseBadRequest, \
    HttpResponseNotFound, HttpResponseForbidden, HttpResponseServerError
import logging
import lxml.etree as etree
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
        ak = hki_geoserver.Asemakaava(username=geoserver_creds.username,
                                            password=geoserver_creds.credential)
        ak_data = ak.get_by_hankenumero(hankenumero)
        if not ak_data:
            log.error("%s not found!" % hankenumero)
            return HttpResponseNotFound()

        log.debug("Hankenumero: %s" % (ak_data['hankenumero']))

        kt = hki_geoserver.Kiinteistotunnus(username=geoserver_creds.username,
                                            password=geoserver_creds.credential)

        kt_data = kt.get_by_geom(ak_data)
        if not kt_data:
            log.error("%s not found!" % hankenumero)
            return HttpResponseNotFound()

        kiinteistot = []
        for kiinteisto in kt_data:
            kiinteisto['geom'] = kt.get_geometry(kiinteisto)

            kt_serializer = KiinteistoV1Serializer(data=kiinteisto)
            if not kt_serializer.is_valid():
                log.error("Invalid WMF-data: %s" % kt_serializer.errors)
                return HttpResponseServerError("Invalid KT data received from WFS!")
            kiinteistot.append(kiinteisto)

        ak_data['geom'] = kt.get_geometry(ak_data)

        ret_data = {
            'asemakaava': ak_data,
            'kiinteistot': kiinteistot,
        }

        return JsonResponse(ret_data)
