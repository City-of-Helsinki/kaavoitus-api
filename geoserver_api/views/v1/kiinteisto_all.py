from rest_framework.views import APIView  # pip install django-rest-framework
from django.http import JsonResponse, HttpResponse, HttpResponseBadRequest, \
    HttpResponseNotFound, HttpResponseForbidden, HttpResponseServerError
from drf_spectacular.openapi import AutoSchema
from drf_spectacular.utils import extend_schema, OpenApiParameter
from drf_spectacular.types import OpenApiTypes
import logging
import lxml.etree as etree
from geoserver_api import hki_geoserver
from ..serializers.v1 import KiinteistoAllV1Serializer
from ..serializers.v1.rakennuskieltov1serializer import RakennuskieltoV1Serializer

log = logging.getLogger(__name__)


class API(APIView):
    serializer_class = KiinteistoAllV1Serializer

    def get(self, request, kiinteistotunnus=None):
        if not kiinteistotunnus:
            return HttpResponseBadRequest("Need kiinteistotunnus!")

        if not request.auth:
            return HttpResponse(status=401)
        geoserver_creds = request.auth.access_geoserver
        if not geoserver_creds:
            return HttpResponseForbidden("No access!")

        # Confirmed access to GeoServer.
        # 1) Go get the data!
        kt = hki_geoserver.Kiinteistotunnus(username=geoserver_creds.username, password=geoserver_creds.credential)
        kt_data = kt.get(kiinteistotunnus)
        if not kt_data:
            log.error("%s not found!" % kiinteistotunnus)
            return HttpResponseNotFound()

        log.debug("Found kiinteistötunnus: %s" % (kt_data['kiinteisto']))
        serializer = self.serializer_class()

        # 2) Which one? Tontti or Maarekisterikiinteistö?
        t = hki_geoserver.Tontti(username=geoserver_creds.username,
                                 password=geoserver_creds.credential)
        t_data = t.get(kiinteistotunnus)
        mr = hki_geoserver.Maarekisterikiinteisto(username=geoserver_creds.username,
                                                  password=geoserver_creds.credential)
        mr_data = mr.get(kiinteistotunnus)
        rekisterilaji = None
        if t_data and mr_data:
            log.warning("Internal: Confusing, which one M or T? %s" % kiinteistotunnus)
        else:
            rekisterilajit = serializer.fields['rekisterilaji'].choices
            if t_data and 'T' in rekisterilajit:
                rekisterilaji = 'T'
            elif mr_data and 'M' in rekisterilajit:
                rekisterilaji = 'M'

        # 3) Asemakaava
        akv = hki_geoserver.Asemakaava_voimassa(username=geoserver_creds.username,
                                                password=geoserver_creds.credential)
        asemakaavan_numero = None
        asemakaava_voimassa = None
        akv_data = akv.get(kt_data)
        if akv_data:
            asemakaavan_numero = akv_data['kaavatunnus']
            asemakaava_voimassa = akv_data['vahvistamispvm']

        # 4) Rakennuskiellot
        rakennuskiellot = []
        rkay = hki_geoserver.Rakennuskieltoalue_yleiskaava(username=geoserver_creds.username,
                                                               password=geoserver_creds.credential)
        rkay_data = rkay.get(kt_data)
        if rkay_data:
            #del rkay_data['geom']
            rkay_data['geom'] = rkay.get_geometry(rkay_data)

            rk_serializer = RakennuskieltoV1Serializer(data=rkay_data)
            if not rk_serializer.is_valid():
                log.error("Invalid WMF-data: %s" % serializer.errors)
                return HttpResponseServerError("Invalid RKAY data received from WFS!")
            rakennuskiellot.append(rkay_data)

        rkaa = hki_geoserver.Rakennuskieltoalue_asemakaava(username=geoserver_creds.username,
                                                           password=geoserver_creds.credential)
        rkaa_data = rkaa.get(kt_data)
        if rkaa_data:
            #del rkaa_data['geom']
            rkaa_data['geom'] = rkaa.get_geometry(rkaa_data)

            rk_serializer = RakennuskieltoV1Serializer(data=rkaa_data)
            if not rk_serializer.is_valid():
                log.error("Invalid WMF-data: %s" % serializer.errors)
                return HttpResponseServerError("Invalid RKAA data received from WFS!")
            rakennuskiellot.append(rkaa_data)

        # Return the data
        ret_data = {
            'kiinteistotunnus': kt_data['kiinteistotunnus'],
            'rekisterilaji': rekisterilaji,
            'asemakaavan_numero': asemakaavan_numero,
            'asemakaava_voimassa': asemakaava_voimassa,
            'rakennuskiellot': rakennuskiellot
        }

        # Go validate the returned data.
        # It needs to be verifiable by serializer rules. Those are published in Swagger.
        serializer = self.serializer_class(data=ret_data)
        if not serializer.is_valid():
            return HttpResponseServerError("Invalid output data!")

        return JsonResponse(serializer.validated_data)
