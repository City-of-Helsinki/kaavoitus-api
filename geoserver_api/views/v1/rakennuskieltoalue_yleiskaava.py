from rest_framework.views import APIView  # pip install django-rest-framework
from django.http import JsonResponse, HttpResponse, HttpResponseBadRequest, \
    HttpResponseNotFound, HttpResponseForbidden, HttpResponseServerError
from drf_spectacular.openapi import AutoSchema
from drf_spectacular.utils import extend_schema, OpenApiParameter
from drf_spectacular.types import OpenApiTypes
import logging
import lxml.etree as etree
from geoserver_api import hki_geoserver
from ..serializers.v1.rakennuskieltov1serializer import RakennuskieltoV1Serializer


log = logging.getLogger(__name__)


class API(APIView):
    serializer_class = RakennuskieltoV1Serializer

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
        kt = hki_geoserver.Kiinteistotunnus(username=geoserver_creds.username,
                                            password=geoserver_creds.credential)
        kt_data = kt.get(kiinteistotunnus)
        if not kt_data:
            log.error("%s not found!" % kiinteistotunnus)
            return HttpResponseNotFound()

        rkay = hki_geoserver.Rakennuskieltoalue_yleiskaava(username=geoserver_creds.username,
                                                           password=geoserver_creds.credential)
        rkay_data = rkay.get(kt_data['geom'])
        if not rkay_data:
            log.warning("%s not found by geom!" % kiinteistotunnus)
            return JsonResponse({})

        del rkay_data['geom']

        # Go validate the returned data.
        # It needs to be verifiable by serializer rules. Those are published in Swagger.
        serializer = self.serializer_class(data=rkay_data)
        if not serializer.is_valid():
            log.error("Invalid WMF-data: %s" % serializer.errors)
            return HttpResponseServerError("Invalid data received from WFS!")

        return JsonResponse(rkay_data)
