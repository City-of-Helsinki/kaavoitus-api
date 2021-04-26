from geoserver_api.hki_geoserver.yleinen_tai_muu_alue import YleinenTaiMuuAlue
from geoserver_api.hki_geoserver.korttelialue import Korttelialue
from rest_framework.views import APIView  # pip install django-rest-framework
from django.http import JsonResponse, HttpResponse, HttpResponseBadRequest, \
    HttpResponseNotFound, HttpResponseForbidden, HttpResponseServerError
import logging
import lxml.etree as etree
from geoserver_api import hki_geoserver
from ..serializers.v1 import SuunnittelualueV1Serializer

log = logging.getLogger(__name__)


class API(APIView):
    serializer_class = SuunnittelualueV1Serializer

    def get(self, request, hankenumero=None):
        if not hankenumero:
            return HttpResponseBadRequest("Need hankenumero!")

        if not request.auth:
            return HttpResponse(status=401)
        self.geoserver_creds = request.auth.access_geoserver
        if not self.geoserver_creds:
            return HttpResponseForbidden("No access!")

        # Confirmed access to GeoServer.
        # Go get the data!
        ak = hki_geoserver.Asemakaava(username=self.geoserver_creds.username,
                                            password=self.geoserver_creds.credential)
        ak_data = ak.get_by_hankenumero(hankenumero)
        if not ak_data:
            log.error("%s not found!" % hankenumero)
            return HttpResponseNotFound()

        log.debug("Hankenumero: %s" % (ak_data['hankenumero']))

        # Convert part of XML-tree from objects to str to be returned as JSON.
        suunnittelualueen_rajaus = etree.tostring(ak_data['geom'].element,
                                  encoding='ascii', method='xml',
                                  xml_declaration=False).decode('ascii')

        keskimaarainen_tonttitehokkuus = self.get_tehokkuusluku(ak_data)
        maanalaisten_tilojen_pinta_ala_yht = self.get_maanalaisten_tilojen_pinta_ala_yht(ak_data)
        aluevarausten_pinta_alat_yht = self.get_aluevarausten_pinta_alat_yht(ak_data)
        pinta_alan_muutokset_yht = self.get_pinta_alan_muutokset_yht()
        suojellut_rakennukset_maara_yht, suojellut_rakennukset_ala_yht = self.get_suojellut_rakennukset(ak_data)

        ret_data = {
            'suunnittelualueen_rajaus': suunnittelualueen_rajaus,
            'suunnittelualueen_pinta_ala': ak_data['pintaala'],
            'keskimaarainen_tonttitehokkuus': keskimaarainen_tonttitehokkuus,
            'maanalaisten_tilojen_pinta_ala_yht': maanalaisten_tilojen_pinta_ala_yht,
            'aluevarausten_pinta_alat_yht': aluevarausten_pinta_alat_yht,
            #'pinta_alan_muutokset_yht': pinta_alan_muutokset_yht,
            'suojellut_rakennukset_maara_yht': suojellut_rakennukset_maara_yht,
            'suojellut_rakennukset_ala_yht': suojellut_rakennukset_ala_yht,
        }

        # Go validate the returned data.
        # It needs to be verifiable by serializer rules. Those are published in Swagger.
        serializer = self.serializer_class(data=ret_data)
        if not serializer.is_valid():
            return HttpResponseServerError("Invalid output data!")

        return JsonResponse(serializer.validated_data)

    def get_tehokkuusluku(self, ak_data):
        t = hki_geoserver.Tontti(username=self.geoserver_creds.username,
                                  password=self.geoserver_creds.credential)
        t_data = t.get_by_geom(ak_data['geom'])
        if not t_data:
            log.error("%s not found!" % ak_data['hankenumero'])
            return HttpResponseNotFound()

        tehokkuus_yht = 0.0
        for tontti in t_data:
            tehokkuusluku = tontti['tehokkuusluku']
            if tehokkuusluku:
                tehokkuus_yht +=  tehokkuusluku

        return tehokkuus_yht / len(t_data)

    def get_maanalaisten_tilojen_pinta_ala_yht(self, ak_data):
        km = hki_geoserver.Kaavamaarays(username=self.geoserver_creds.username,
                                            password=self.geoserver_creds.credential)
        km_data = km.get_by_geom(ak_data['geom'])
        if not km_data:
            log.warning("%s not found by geom!" % ak_data['hankenumero'])
            return JsonResponse({})

        maanalainen = 0.0
        for km in km_data:
            if km['maanalainen'] and km['pintaala']:
                maanalainen += float(km['pintaala'])

        return maanalainen

    def get_aluevarausten_pinta_alat_yht(self, ak_data):
        ka = Korttelialue(username=self.geoserver_creds.username, password=self.geoserver_creds.credential)
        ka_data = ka.get_by_geom(ak_data['geom'])
        if not ka_data:
            log.error("%s not found!" % ak_data['hankenumero'])
            return HttpResponseNotFound()

        pinta_ala = 0.0
        for ka in ka_data:
            if ka['pintaala']:
                pinta_ala += float(ka['pintaala'])

        ya = YleinenTaiMuuAlue(username=self.geoserver_creds.username, password=self.geoserver_creds.credential)
        ya_data = ya.get_by_geom(ak_data['geom'])
        if not ya_data:
            log.error("%s not found!" % ak_data['hankenumero'])
            return HttpResponseNotFound()

        for ya in ya_data:
            if ya['pintaala']:
                pinta_ala += float(ka['pintaala'])

        return pinta_ala

    def get_pinta_alan_muutokset_yht(self):
        return ''

    def get_suojellut_rakennukset(self, ak_data):
        ra = hki_geoserver.Rakennusala(username=self.geoserver_creds.username,
                                                password=self.geoserver_creds.credential)
        ra_data = ra.get_by_geom(ak_data['geom'])
        if not ra_data:
            log.warning("%s not found by geom!" % ak_data['hankenumero'])
            return JsonResponse({})

        maara = 0
        ala = 0.0
        for ra in ra_data:
            if ra['kaavamerkinta'] is 's' or \
               ra['kaavamerkinta'] is 'sr' or \
               ra['kaavamerkinta'] is 'sr-1' or \
               ra['kaavamerkinta'] is 'sr-2' or \
               ra['kaavamerkinta'] is 'sr-3':
                maara += 1
                if ra['pintaala']:
                    ala += float(ra['pintaala']) # ra['km2']?

        return maara, ala
