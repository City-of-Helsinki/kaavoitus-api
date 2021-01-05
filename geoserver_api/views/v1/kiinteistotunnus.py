from rest_framework.views import APIView  # pip install django-rest-framework
from django.http import JsonResponse, HttpResponse, HttpResponseBadRequest, \
    HttpResponseNotFound, HttpResponseForbidden, HttpResponseServerError
from drf_spectacular.openapi import AutoSchema
from drf_spectacular.utils import extend_schema, OpenApiParameter
from drf_spectacular.types import OpenApiTypes
import logging
import lxml.etree as etree
from geoserver_api.hki_geoserver.kiinteistotunnus import Kiinteistotunnus
from geoserver_api.views.serializers.v1 import KiinteistoV1Serializer

log = logging.getLogger(__name__)


class API(APIView):
    serializer_class = KiinteistoV1Serializer

    def get(self, request, id=None):
        if not id:
            return HttpResponseBadRequest("Need id!")

        if not request.auth:
            return HttpResponse(status=401)
        geoserver_creds = request.auth.access_geoserver
        if not geoserver_creds:
            return HttpResponseForbidden("No access!")

        # Confirmed access to GeoServer.
        # Go get the data!
        kt = Kiinteistotunnus(username=geoserver_creds.username, password=geoserver_creds.credential)
        kt_data = kt.get(id)
        if not kt_data:
            log.error("%s not found!" % id)
            return HttpResponseNotFound()

        log.info("Kiinteistötunnus: %s" % (kt_data['kiinteisto']))
        # Convert part of XML-tree from objects to str to be returned as JSON.
        geom_str = etree.tostring(kt_data['geom'].element,
                                  encoding='ascii', method='xml',
                                  xml_declaration=False).decode('ascii')
        kt_data['geom'] = geom_str

        # Go validate the returned data.
        # It needs to be verifiable by serializer rules. Those are published in Swagger.
        serializer = self.serializer_class(data=kt_data)
        if not serializer.is_valid():
            return HttpResponseServerError("Invalid data received from WFS!")

        return JsonResponse(serializer.validated_data)

    @extend_schema(responses={200: OpenApiTypes.OBJECT})
    def post(self, request):
        pass
