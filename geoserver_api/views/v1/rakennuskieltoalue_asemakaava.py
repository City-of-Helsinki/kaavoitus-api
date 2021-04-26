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

        rkaa = hki_geoserver.Rakennuskieltoalue_asemakaava(username=geoserver_creds.username,
                                                           password=geoserver_creds.credential)
        rkaa_data = rkaa.get(kt_data['geom'])
        if not rkaa_data:
            log.warning("%s not found by geom!" % kiinteistotunnus)
            return JsonResponse({})

        #del rkaa_data['geom']
        # Convert part of XML-tree from objects to str to be returned as JSON.
        geom_str = etree.tostring(rkaa_data['geom'].element,
                                  encoding='ascii', method='xml',
                                  xml_declaration=False).decode('ascii')
        rkaa_data['geom'] = geom_str

        # Go validate the returned data.
        # It needs to be verifiable by serializer rules. Those are published in Swagger.
        serializer = self.serializer_class(data=rkaa_data)
        if not serializer.is_valid():
            log.error("Invalid WMF-data: %s" % serializer.errors)
            return HttpResponseServerError("Invalid data received from WFS!")

        return JsonResponse(rkaa_data)
