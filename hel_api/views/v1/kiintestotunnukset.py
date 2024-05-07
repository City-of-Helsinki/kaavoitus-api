import requests
import logging

from django.http import (
    JsonResponse,
    HttpResponseBadRequest,
    HttpResponseServerError,
)
from requests.exceptions import HTTPError, Timeout
from rest_framework.views import APIView
from hel_api.views.serializers.v1 import KiinteistotunnusV1Serializer
from hel_api.views.helpers import build_apila_url

log = logging.getLogger(__name__)

wfsKiinteistoLajit = ["hel:Kiinteisto_alue_tontti", "hel:Kiinteisto_alue_maarekisterikiinteisto", "hel:Kiinteisto_alue_yleinen_alue"]


class API(APIView):
    serializer_class = KiinteistotunnusV1Serializer

    def get(self, request, hankenumero):
        if not hankenumero:
            return HttpResponseBadRequest("Need hankenumero!")

        try:
            data = self.get_data(hankenumero)
            serializer = self.serializer_class(data=data)
            if not serializer.is_valid():
                return HttpResponseServerError("Invalid data!")
            return JsonResponse(data=serializer.validated_data)
        except Exception as exc:
            log.error('Error getting kiinteistotunnukset from Apila WFS API', exc)
            return HttpResponseServerError("Error getting kiinteistotunnukset from Apila WFS API")

    def get_data(self, hankenumero):
        kiinteistotunnukset = []
        for kiinteistolaji in wfsKiinteistoLajit:
            leikkaavat = self.get_kiinteistotunnukset(build_apila_url(kiinteistolaji, hankenumero, "intersects"))
            koskettavat = self.get_kiinteistotunnukset(build_apila_url(kiinteistolaji, hankenumero, "touches"))
            kiinteistotunnukset.extend(self.sisallytaVainKaavaanKuuluvatKiinteistot(leikkaavat, koskettavat))

        return {
            "hankenumero": hankenumero,
            "kiinteistotunnukset": kiinteistotunnukset
        }

    def get_kiinteistotunnukset(self, url):
        try:
            kiinteistot = requests.get(url, timeout=5).json()
            kiinteistotunnukset = []
            for kiinteisto in kiinteistot["features"]:
                kunta = kiinteisto["properties"]["kunta"]
                sijaintialue = kiinteisto["properties"]["sijaintialue"]
                ryhma = kiinteisto["properties"]["ryhma"]
                yksikko = kiinteisto["properties"]["yksikko"]
                # Yhdistetään kiinteistötunnus tekstiksi muotoon kunta-sijaintialue-ryhma-yksikko
                # Yhtenäinen kiinteistötunnus ilman väliviivaa löytyisi kohdasta ["properties"]["kiinteistotunnus"]
                kiinteistotunnukset.append(kunta + "-" + sijaintialue + "-" + ryhma + "-" + yksikko)
            return kiinteistotunnukset
        except Timeout as timeout:
            logging.error('Timeout occurred', timeout)
            raise
        except HTTPError as http_err:
            logging.error('HTTP error occurred', http_err)
            raise
        except Exception as err:
            logging.error('Other error occurred', err)
            raise

    def sisallytaVainKaavaanKuuluvatKiinteistot(self, leikkaavatKiinteistotunnukset, koskettavatKiinteistotunnukset):
        kiinteistotunnukset = []
        for kiinteistotunnus in leikkaavatKiinteistotunnukset:
            if kiinteistotunnus not in koskettavatKiinteistotunnukset:
                kiinteistotunnukset.append(kiinteistotunnus)
        return kiinteistotunnukset
