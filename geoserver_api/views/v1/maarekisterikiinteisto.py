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
        mr = hki_geoserver.Maarekisterikiinteisto(username=geoserver_creds.username,
                                            password=geoserver_creds.credential)
        mr_data = mr.get(id)
        if not mr_data:
            log.error("%s not found!" % id)
            return HttpResponseNotFound()

        geom_str = etree.tostring(mr_data['geom'].element,
                                  encoding='ascii', method='xml',
                                  xml_declaration=False).decode('ascii')
        mr_data['geom'] = geom_str

        return JsonResponse(mr_data)
