from rest_framework.views import APIView  # pip install django-rest-framework
from django.http import JsonResponse, HttpResponse, HttpResponseBadRequest, \
    HttpResponseNotFound, HttpResponseForbidden, HttpResponseServerError
from drf_spectacular.openapi import AutoSchema
from drf_spectacular.utils import extend_schema, OpenApiParameter
from drf_spectacular.types import OpenApiTypes
import logging
import lxml.etree as etree
from geoserver_api import hki_geoserver

log = logging.getLogger(__name__)


class API(APIView):

    def get(self, request, kaavatunnus=None):
        if not kaavatunnus:
            return HttpResponseBadRequest("Need kaavatunnus!")

        if not request.auth:
            return HttpResponse(status=401)
        geoserver_creds = request.auth.access_geoserver
        if not geoserver_creds:
            return HttpResponseForbidden("No access!")

        # Confirmed access to GeoServer.
        # Go get the data!
        ak = hki_geoserver.Asemakaava(username=geoserver_creds.username,
                                            password=geoserver_creds.credential)
        ak_data = ak.get(kaavatunnus)
        if not ak_data:
            log.error("%s not found!" % kaavatunnus)
            return HttpResponseNotFound()

        log.debug("Kaavatunnus: %s" % (ak_data['kaavatunnus']))
        # Convert part of XML-tree from objects to str to be returned as JSON.
        geom_str = etree.tostring(ak_data['geom'].element,
                                  encoding='ascii', method='xml',
                                  xml_declaration=False).decode('ascii')
        ak_data['geom'] = geom_str

        return JsonResponse(ak_data)

