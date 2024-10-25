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
from hel_api.views.serializers.v1 import KaavatV1Serializer
from hel_api.views.helpers import build_apila_url

log = logging.getLogger(__name__)

wfsKaavalajit = ["hel:Kaavahakemisto_alue_maanalainenkaava_voimassa", "hel:Kaavahakemisto_alue_kaava_voimassa"]


class API(APIView):
    serializer_class = KaavatV1Serializer

    def get(self, request, hankenumero):
        if not hankenumero:
            return HttpResponseBadRequest("Need hankenumero!")

        try:
            data = self.get_data(hankenumero)
            serializer = self.serializer_class(data=data)
            if not serializer.is_valid():
                return HttpResponseServerError("Invalid data!")
            return JsonResponse(data=serializer.validated_data, safe=False)
        except Exception:
            log.error('Error getting kaavat from Apila WFS API')
            return HttpResponseServerError("Error getting kaavat from Apila WFS API")

    def get_data(self, hankenumero):
        kaavatunnukset = []
        for kaavalaji in wfsKaavalajit:
            leikkaavatKaavat = self.get_kaavat(build_apila_url(kaavalaji, hankenumero, "intersects"))
            koskettavatKaavat = self.get_kaavat(build_apila_url(kaavalaji, hankenumero, "touches"))
            if leikkaavatKaavat:
                kaavatunnukset.extend(self.sisallytaVainKaavaanKuuluvatKaavat(leikkaavatKaavat, koskettavatKaavat))

        return {
            "hankenumero": hankenumero,
            "kaavat": [
                {
                    "kaavatunnus": kaava[0],
                    "date": kaava[1],
                    "date_type": kaava[2],
                } for kaava in kaavatunnukset
            ]
        }

    def get_kaavat(self, url):
        try:
            root = ElementTree.fromstring(requests.get(url, timeout=10).content)
            kaavatunnukset = []
            for member in root:
                for kaava in member:
                    kaavatunnus = kaava.find('{http://www.hel.fi/hel}kaavatunnus').text
                    if kaava.find('{http://www.hel.fi/hel}lainvoimaisuuspvm') is not None:
                        pvm = kaava.find('{http://www.hel.fi/hel}lainvoimaisuuspvm').text
                        pvmTarkoitus = "lainvoimaisuuspvm"
                    else:
                        pvm = kaava.find('{http://www.hel.fi/hel}vahvistamispvm').text
                        pvmTarkoitus = "vahvistamispvm"
                    kaavatunnukset.append([kaavatunnus, pvm, pvmTarkoitus])
            return kaavatunnukset
        except Timeout as timeout:
            logging.error('Timeout occurred', timeout)
        except HTTPError as http_err:
            logging.error(f'HTTP error occurred' ,http_err)
        except Exception as err:
            logging.error(f'Other error occurred', err)
        return []

    def sisallytaVainKaavaanKuuluvatKaavat(self, leikkaavatKaavatunnukset, koskettavatKaavatunnukset):
        kaavatunnukset = []
        for kaavatunnus in leikkaavatKaavatunnukset:
            if kaavatunnus not in koskettavatKaavatunnukset:
                kaavatunnukset.append(kaavatunnus)
        return kaavatunnukset
