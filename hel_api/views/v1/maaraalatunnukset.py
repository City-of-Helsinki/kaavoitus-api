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
from hel_api.views.serializers.v1 import MaaraalatunnusV1Serializer
from hel_api.views.helpers import build_apila_url, sisallyta_vain_kaavaan_kuuluvat

log = logging.getLogger(__name__)

wfsMaaraalaLajit = ["hel:Maaraala_alue_epavarma_sijainti", "hel:Maaraala_alue_varma_sijainti", "hel:Maaraala_alue_arvioitu_sijainti"]


class API(APIView):
    serializer_class = MaaraalatunnusV1Serializer

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
            log.error('Error getting maaraalatunnukset from Apila WFS API', exc)
            return HttpResponseServerError("Error getting maaraalatunnukset from Apila WFS API")

    def get_data(self, hankenumero):
        maaraalatunnukset = []
        for maaraLaji in wfsMaaraalaLajit:
            leikkaavat = self.get_maaraalatunnukset(build_apila_url(maaraLaji, hankenumero, "intersects"))
            koskettavat = self.get_maaraalatunnukset(build_apila_url(maaraLaji, hankenumero, "touches"))
            maaraalatunnukset.extend(sisallyta_vain_kaavaan_kuuluvat(leikkaavat, koskettavat))

        return {
            "hankenumero": hankenumero,
            "maaraalatunnukset": maaraalatunnukset
        }

    def get_maaraalatunnukset(self, url):
        try:
            root = ElementTree.fromstring(requests.get(url, timeout=10).content)
            maaraalatunnukset = []
            for member in root:
                for maaraala in member:
                    kunta = maaraala.find('{http://www.hel.fi/hel}kunta').text
                    sijaintialue = maaraala.find('{http://www.hel.fi/hel}sijaintialue').text
                    ryhma = maaraala.find('{http://www.hel.fi/hel}ryhma').text
                    yksikko = maaraala.find('{http://www.hel.fi/hel}yksikko').text
                    tunnus_kirjainosa = maaraala.find('{http://www.hel.fi/hel}tunnus_kirjainosa').text
                    tunnus = maaraala.find('{http://www.hel.fi/hel}tunnus').text
                    maaraalatunnukset.append(kunta + "-" + sijaintialue + "-" + ryhma + "-" + yksikko + "-" + tunnus_kirjainosa + "" + tunnus)
            return maaraalatunnukset
        except Timeout as timeout:
            logging.error('Timeout occurred', timeout)
            raise
        except HTTPError as http_err:
            logging.error('HTTP error occurred', http_err)
            raise
        except Exception as err:
            logging.error('Other error occurred', err)
            raise