import requests
import logging
from xml.etree import ElementTree

from django.http import (
    JsonResponse,
    HttpResponseBadRequest,
    HttpResponseServerError,
)
from requests.exceptions import HTTPError, Timeout
from rest_framework.views import APIView
from hel_api.views.serializers.v1 import KiinteistotunnusV1Serializer
from hel_api.views.helpers import build_apila_url, sisallyta_vain_kaavaan_kuuluvat

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
            kiinteistotunnukset.extend(sisallyta_vain_kaavaan_kuuluvat(leikkaavat, koskettavat))

        return {
            "hankenumero": hankenumero,
            "kiinteistotunnukset": kiinteistotunnukset
        }

    def get_kiinteistotunnukset(self, url):
        try:
            root = ElementTree.fromstring(requests.get(url, timeout=10).content)
            kiinteistotunnukset = []
            for member in root:
                for kiinteisto in member:
                    kunta = kiinteisto.find('{http://www.hel.fi/hel}kunta').text
                    sijaintialue = kiinteisto.find('{http://www.hel.fi/hel}sijaintialue').text
                    ryhma = kiinteisto.find('{http://www.hel.fi/hel}ryhma').text
                    yksikko = kiinteisto.find('{http://www.hel.fi/hel}yksikko').text
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
