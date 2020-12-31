from rest_framework.views import APIView  # pip install django-rest-framework
from django.http import JsonResponse, HttpResponseBadRequest, HttpResponseNotFound
from drf_spectacular.openapi import AutoSchema
from drf_spectacular.utils import extend_schema, OpenApiParameter
from drf_spectacular.types import OpenApiTypes
import logging
import lxml.etree as etree
from kaavapino_api.hki_geoserver.kiinteistotunnus import Kiinteistotunnus

log = logging.getLogger(__name__)


class API(APIView):
    def get(self, request, id=None):
        if not id:
            return HttpResponseBadRequest("Need id!")

        kt = Kiinteistotunnus()
        kt_data = kt.get(id)
        if not kt_data:
            log.error("%s not found!")
            return HttpResponseNotFound()

        log.info("Kiinteistötunnus: %s" % (kt_data['kiinteisto']))
        geom_str = etree.tostring(kt_data['geom'].element,
                                  encoding='ascii', method='xml',
                                  xml_declaration=False).decode('ascii')
        kt_data['geom'] = geom_str

        return JsonResponse(kt_data, content_type="application/json")

    @extend_schema(responses={200: OpenApiTypes.OBJECT})
    def post(self, request):
        pass
