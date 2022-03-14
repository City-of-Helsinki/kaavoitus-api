from geoserver_api.hki_geoserver.yleinen_tai_muu_alue import YleinenTaiMuuAlue
from geoserver_api.hki_geoserver.korttelialue import Korttelialue
from rest_framework.views import APIView  # pip install django-rest-framework
from django.http import (
    JsonResponse,
    HttpResponse,
    HttpResponseBadRequest,
    HttpResponseNotFound,
    HttpResponseForbidden,
    HttpResponseServerError,
)
import logging
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
        kh = hki_geoserver.Kaavahanke(
            username=self.geoserver_creds.username,
            password=self.geoserver_creds.credential,
        )
        data = kh.get_by_hankenumero(hankenumero)
        if not data:
            log.error("Kaavahanke (%s) not found!" % hankenumero)
            # TODO: is this required?
            # Try with asemakaava
            ak = hki_geoserver.Asemakaava(
                username=self.geoserver_creds.username,
                password=self.geoserver_creds.credential,
            )
            data = ak.get_by_hankenumero(hankenumero)
            ak_data = data
            if not data:
                log.error("Asemakaava (%s) not found!" % hankenumero)
                return HttpResponseNotFound()
        else:
            ak = hki_geoserver.Asemakaava(
                username=self.geoserver_creds.username,
                password=self.geoserver_creds.credential,
            )
            ak_data = ak.get_by_hankenumero(hankenumero)

        log.info("Hankenumero: %s" % (data.get("hankenumero")))

        suunnittelualueen_rajaus = ak.get_geometry(data)

        keskimaarainen_tonttitehokkuus = self.get_tehokkuusluku(data)
        maanalaisten_tilojen_pinta_ala_yht = None
        # maanalaisten_tilojen_pinta_ala_yht = (
        #     self.get_maanalaisten_tilojen_pinta_ala_yht(data)
        # )
        aluevarausten_pinta_alat_yht = None
        # aluevarausten_pinta_alat_yht = self.get_aluevarausten_pinta_alat_yht(data)
        pinta_alan_muutokset_yht = self.get_pinta_alan_muutokset_yht()
        # (
        #     suojellut_rakennukset_maara_yht,
        #     suojellut_rakennukset_ala_yht,
        # ) = self.get_suojellut_rakennukset(data)
        suojellut_rakennukset_maara_yht = None
        suojellut_rakennukset_ala_yht = None

        ret_data = {
            "suunnittelualueen_rajaus": suunnittelualueen_rajaus,
            "suunnittelualueen_pinta_ala": ak_data.get("pintaala") if ak_data else 0.0,
            "keskimaarainen_tonttitehokkuus": keskimaarainen_tonttitehokkuus,
            "maanalaisten_tilojen_pinta_ala_yht": maanalaisten_tilojen_pinta_ala_yht,
            "aluevarausten_pinta_alat_yht": aluevarausten_pinta_alat_yht,
            "pinta_alan_muutokset_yht": pinta_alan_muutokset_yht,
            "suojellut_rakennukset_maara_yht": suojellut_rakennukset_maara_yht,
            "suojellut_rakennukset_ala_yht": suojellut_rakennukset_ala_yht,
        }

        # Go validate the returned data.
        # It needs to be verifiable by serializer rules. Those are published in Swagger.
        serializer = self.serializer_class(data=ret_data)
        if not serializer.is_valid():
            return HttpResponseServerError("Invalid output data!")

        return JsonResponse(serializer.validated_data)

    def get_tehokkuusluku(self, ak_data):
        t = hki_geoserver.Tontti(
            username=self.geoserver_creds.username,
            password=self.geoserver_creds.credential,
        )

        tehokkuus_yht = 0.0
        t_data = t.get_by_geom(ak_data)
        if not t_data:
            log.error("Tontti (%s) not found!" % ak_data.get("hankenumero"))
            return tehokkuus_yht

        for tontti in t_data:
            # log.info(tontti)
            # key missing from json
            if tontti.get("tehokkuusluku"):
                tehokkuus_yht += tontti.get("tehokkuusluku")

        return tehokkuus_yht / len(t_data)

    def get_maanalaisten_tilojen_pinta_ala_yht(self, ak_data):
        km = hki_geoserver.Kaavamaarays(
            username=self.geoserver_creds.username,
            password=self.geoserver_creds.credential,
        )

        maanalainen = 0.0
        km_data = km.get_by_geom(ak_data)
        if not km_data:
            log.warning(
                "Kaavamaarays (%s) not found by geom!" % ak_data.get("hankenumero")
            )
            return maanalainen

        for kmd in km_data:
            if kmd.get("maanalainen") and kmd.get("pintaala"):
                maanalainen += float(kmd.get("pintaala"))

        return maanalainen

    def get_aluevarausten_pinta_alat_yht(self, ak_data):
        ka = Korttelialue(
            username=self.geoserver_creds.username,
            password=self.geoserver_creds.credential,
        )

        pinta_ala = 0.0
        ka_data = ka.get_by_geom(ak_data)
        if not ka_data:
            log.error("Korttelialue (%s) not found!" % ak_data.get("hankenumero"))
            return pinta_ala

        for kad in ka_data:
            if kad.get("pintaala"):
                pinta_ala += float(kad.get("pintaala"))

        ya = YleinenTaiMuuAlue(
            username=self.geoserver_creds.username,
            password=self.geoserver_creds.credential,
        )

        ya_data = ya.get_by_geom(ak_data)
        if not ya_data:
            log.error("YleinenTaiMuuAlue (%s) not found!" % ak_data.get("hankenumero"))
            return pinta_ala

        for yad in ya_data:
            if yad.get("pintaala"):
                pinta_ala += float(yad.get("pintaala"))

        return pinta_ala

    def get_pinta_alan_muutokset_yht(self):
        return 0.0

    def get_suojellut_rakennukset(self, ak_data):
        ra = hki_geoserver.Rakennusala(
            username=self.geoserver_creds.username,
            password=self.geoserver_creds.credential,
        )

        maara = 0
        ala = 0.0
        ra_data = ra.get_by_geom(ak_data)
        if not ra_data:
            log.warning(
                "Rakennusala (%s) not found by geom!" % ak_data.get("hankenumero")
            )
            return maara, ala

        for rad in ra_data:
            if (
                rad.get("kaavamerkinta") == "s"
                or rad.get("kaavamerkinta") == "sr"
                or rad.get("kaavamerkinta") == "sr-1"
                or rad.get("kaavamerkinta") == "sr-2"
                or rad.get("kaavamerkinta") == "sr-3"
            ):
                maara += 1
                if rad.get("pintaala"):
                    ala += float(rad.get("pintaala"))  # ra.get('km2')?

        return maara, ala
