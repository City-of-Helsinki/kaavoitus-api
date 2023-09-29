from django.http.response import (
    HttpResponseServerError
)
from django.http import (
    JsonResponse,
    HttpResponseBadRequest,
)
import logging
import requests
from requests.exceptions import HTTPError
from hel_api.views.serializers.v1.paikkatietov1serializer import PaikkatietoV1Serializer
from rest_framework.views import APIView
from django.conf import settings
from django.core.cache import cache

from geoserver_api import hki_geoserver
from facta_api import hel_facta

log = logging.getLogger(__name__)
wfsKiinteistoLajit = ["hel:Kiinteisto_alue_tontti", "hel:Kiinteisto_alue_maarekisterikiinteisto", "hel:Kiinteisto_alue_yleinen_alue"]


def build_url(kiinteistolaji, hankenumero, cql_filter):
    url = settings.APILA_URL \
        + "?SERVICE=WFS&VERSION=2.0.0&REQUEST=GetFeature&TYPENAMES=" + kiinteistolaji \
        + ("&CQL_FILTER=" + cql_filter if cql_filter else "") \
        + "(geom,querySingle('hel:asemakaava','geom','kaavatunnus=''" + hankenumero + "'''))" \
        + "&outputFormat=application/json"
    return url


def get_kiinteistotunnukset(url):
    try:
        kiinteistot = requests.get(url).json()
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
    except HTTPError as http_err:
        logging.error('HTTP error occurred', http_err)
    except Exception as err:
        logging.error('Other error occurred', err)
    return []


def sisallytaVainKaavaanKuuluvatKiinteistot(leikkaavatKiinteistotunnukset, koskettavatKiinteistotunnukset):
    kiinteistotunnukset = []
    for kiinteistotunnus in leikkaavatKiinteistotunnukset:
        if kiinteistotunnus not in koskettavatKiinteistotunnukset:
            kiinteistotunnukset.append(kiinteistotunnus)
    return kiinteistotunnukset


class API(APIView):
    serializer_class = PaikkatietoV1Serializer

    def get(self, request, hankenumero):
        if not hankenumero:
            return HttpResponseBadRequest("Need hankenumero!")

        kiinteistotunnukset = []
        for kiinteistolaji in wfsKiinteistoLajit:
            leikkaavat = get_kiinteistotunnukset(build_url(kiinteistolaji, hankenumero, "intersects"))
            koskettavat = get_kiinteistotunnukset(build_url(kiinteistolaji, hankenumero, "touches"))
            kiinteistotunnukset.extend(sisallytaVainKaavaanKuuluvatKiinteistot(leikkaavat, koskettavat))

        asemakaavat = {}
        rakennuskiellot = {}
        # Data should reflect the field names defined in Kaavaprojektitiedot excel 'projektitieto tunniste' column
        data = {
            "voimassa_asemakaavat_fieldset": [],
            "voimassa_olevat_rakennuskiellot_fieldset": [],
            "maanomistus_kaupunki": "Ei",
            "maanomistus_valtio": "Ei",
            "maanomistus_yksityinen": "Ei",
            "maanomistaja_ulkopaikkakunta": "Ei",
            "haltija_ulkopaikkakunta": "Ei"
        }

        geoserver_creds = request.auth.access_geoserver
        if geoserver_creds:
            kt = hki_geoserver.Kiinteistotunnus(
                username=geoserver_creds.username, password=geoserver_creds.credential
            )
            for kiinteistotunnus in kiinteistotunnukset:
                formatted_kt = "".join(kiinteistotunnus.split("-"))
                kt_data = kt.get(formatted_kt)
                if not kt_data:
                    log.error(f'Failed to get kt_data for kiinteistotunnus {formatted_kt}')
                    continue

                # Asemakaava
                akv = hki_geoserver.Asemakaava_voimassa(
                    username=geoserver_creds.username, password=geoserver_creds.credential
                )
                akv_data = akv.get_by_geom(kt_data, single_result=True)
                if akv_data:
                    asemakaavat[akv_data["kaavatunnus"]] = akv_data["vahvistamispvm"]

                # Rakennuskiellot
                rkay = hki_geoserver.Rakennuskieltoalue_yleiskaava(
                    username=geoserver_creds.username, password=geoserver_creds.credential
                )
                rkay_data = rkay.get_by_geom(kt_data, single_result=True)
                if rkay_data:
                    rakennuskiellot[rkay_data["rakennuskieltotunnus"]] = rkay_data["laatu_selite"]

                rkaa = hki_geoserver.Rakennuskieltoalue_asemakaava(
                    username=geoserver_creds.username, password=geoserver_creds.credential
                )
                rkaa_data = rkaa.get_by_geom(kt_data, single_result=True)
                if rkaa_data:
                    rakennuskiellot[rkaa_data["rakennuskieltotunnus"]] = rkaa_data["laatu_selite"]

                data["voimassa_asemakaavat_fieldset"] = [
                    {
                        "voimassa_asemakaava_numero": ak_numero,
                        "milloin_asemakaava_tullut_voimaan": ak_voimassa
                    } for ak_numero, ak_voimassa in asemakaavat.items()
                ]
                data["voimassa_olevat_rakennuskiellot_fieldset"] = [
                    {
                        "rakennuskiellon_numero": rk_numero,
                        "rakennuskiellon_peruste": rk_peruste
                    } for rk_numero, rk_peruste in rakennuskiellot.items()
                ]

                # Kiinteistönomistajat
                f_ko = hel_facta.KiinteistonOmistajat()

                cache_key = f'paikkatieto_kiinteistonomistajat_{kiinteistotunnus}'
                owner_rows = cache.get(cache_key)
                if not owner_rows:
                    owner_rows = f_ko.get_by_kiinteistotunnus(kiinteistotunnus)
                    cache.set(cache_key, owner_rows, settings.FACTA_CACHE_TIMEOUT)

                if owner_rows:
                    for owner_row in owner_rows:
                        if owner_row[14] == "10":  # C_LAJI
                            # Helsinki
                            data["maanomistus_kaupunki"] = "Kyllä"
                        elif owner_row[14] in ["8", "11"]:  # C_LAJI
                            # Govt. of Finland
                            data["maanomistus_valtio"] = "Kyllä"
                        else:
                            # Private
                            data["maanomistus_yksityinen"] = "Kyllä"

                        if owner_row[17] != "091":
                            data["maanomistaja_ulkopaikkakunta"] = "Kyllä"

                # Kiinteistönhaltijat
                f_kh = hel_facta.KiinteistonHaltijat()

                cache_key = f'paikkatieto_kiinteistonhaltijat_{kiinteistotunnus}'
                occupant_rows = cache.get(cache_key)
                if not occupant_rows:
                    occupant_rows = f_kh.get_by_kiinteistotunnus(kiinteistotunnus)
                    cache.set(cache_key, occupant_rows, settings.FACTA_CACHE_TIMEOUT)

                if occupant_rows:
                    for occupant_row in occupant_rows:
                        if occupant_row[27] != "HELSINKI" and occupant_row[27] != "HELSINGIN KAUPUNKI":
                            data["haltija_ulkopaikkakunta"] = "Kyllä"
                            break

        serializer = self.serializer_class(data=data)
        if not serializer.is_valid():
            return HttpResponseServerError("Invalid data!")

        return JsonResponse(data=serializer.validated_data)
