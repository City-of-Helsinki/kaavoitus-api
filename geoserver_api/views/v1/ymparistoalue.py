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

        ya = hki_geoserver.Ymparistoalue(username=geoserver_creds.username,
                                                password=geoserver_creds.credential)
        ya_data = ya.get(kt_data['geom'])
        if not ya_data:
            log.warning("%s not found by geom!" % kiinteistotunnus)
            return JsonResponse({})

        del ya_data['geom']

        return JsonResponse(ya_data)
