from rest_framework.views import APIView  # pip install django-rest-framework
from django.http import JsonResponse, HttpResponse, HttpResponseBadRequest, \
    HttpResponseNotFound, HttpResponseForbidden
import logging
import lxml.etree as etree
from kaavapino_api import hki_geoserver

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
        t = hki_geoserver.Tontti(username=geoserver_creds.username,
                                  password=geoserver_creds.credential)
        t_data = t.get(id)
        if not t_data:
            log.error("%s not found!" % id)
            return HttpResponseNotFound()

        geom_str = etree.tostring(t_data['geom'].element,
                                  encoding='ascii', method='xml',
                                  xml_declaration=False).decode('ascii')
        t_data['geom'] = geom_str

        return JsonResponse(t_data)
