import requests
import logging

from django.http import (
    JsonResponse,
    HttpResponseBadRequest,
    HttpResponseServerError,
)
from requests.exceptions import HTTPError, Timeout
from rest_framework.views import APIView
from hel_api.views.serializers.v1 import RakennuskiellotV1Serializer
from hel_api.views.helpers import build_apila_url

log = logging.getLogger(__name__)

wfsRakennuskieltolajit = ["hel:Rakennuskieltoalue_asemakaavan_laatimiseksi", "hel:Rakennuskieltoalue_yleiskaavan_laatimiseksi"]


class API(APIView):
    serializer_class = RakennuskiellotV1Serializer

    def get(self, request, hankenumero):
        if not hankenumero:
            return HttpResponseBadRequest("Need hankenumero!")

        try:
            data = self.get_data(hankenumero)
            serializer = self.serializer_class(data=data)
            if not serializer.is_valid():
                return HttpResponseServerError("Invalid data!")
            return JsonResponse(data=serializer.validated_data)
        except Exception:
            log.error('Error getting rakennuskiellot from Apila WFS API')
            return HttpResponseServerError("Error getting rakennuskiellot from Apila WFS API")

    def get_data(self, hankenumero):
        rakennuskiellot = []
        for rakennuskieltolaji in wfsRakennuskieltolajit:
            leikkaavat = self.get_rakennuskiellot(build_apila_url(rakennuskieltolaji, hankenumero, "intersects"))
            koskettavat = self.get_rakennuskiellot(build_apila_url(rakennuskieltolaji, hankenumero, "touches"))
            rakennuskiellot.extend(self.sisallytaVainKaavaanKuuluvatRakennuskiellot(leikkaavat, koskettavat))

        return {
            "hankenumero": hankenumero,
            "rakennuskiellot": [
                {
                    "rakennuskieltotunnus": rakennuskielto[0],
                    "date": rakennuskielto[1],
                    "date_type": rakennuskielto[2],
                    "selite": rakennuskielto[3]
                } for rakennuskielto in rakennuskiellot
            ]
        }

    def get_rakennuskiellot(self, url):
        try:
            rakennuskiellot = requests.get(url).json()
            rakennuskieltotunnukset = []
            for rakennuskielto in rakennuskiellot["features"]:
                rakennuskieltotunnus = rakennuskielto["properties"]["rakennuskieltotunnus"]
                pvm = rakennuskielto["properties"]["voimaantulopvm"]
                pvmTarkoitus = "voimaantulopvm"
                selite = rakennuskielto["properties"]["laatu_selite"]
                rakennuskieltotunnukset.append([rakennuskieltotunnus, pvm, pvmTarkoitus, selite])
            return rakennuskieltotunnukset
        except Timeout as timeout:
            logging.error('Timeout occurred', timeout)
            raise
        except HTTPError as http_err:
            print(f'HTTP error occurred: {http_err}')
        except Exception as err:
            print(f'Other error occurred: {err}')

    def sisallytaVainKaavaanKuuluvatRakennuskiellot(self, leikkaavatRakennuskieltotunnukset, koskettavatRakennuskieltotunnukset):
        rakennuskieltotunnukset = []
        for rakennuskieltotunnus in leikkaavatRakennuskieltotunnukset:
            if rakennuskieltotunnus not in koskettavatRakennuskieltotunnukset:
                rakennuskieltotunnukset.append(rakennuskieltotunnus)
        return rakennuskieltotunnukset

