from django.http.response import (
    HttpResponseServerError
)
from django.http import (
    JsonResponse,
    HttpResponseBadRequest,
)
import logging
from hel_api.views.serializers.v1.paikkatietov1serializer import PaikkatietoV1Serializer
from rest_framework.views import APIView
from django.conf import settings
from django.core.cache import cache

from facta_api import hel_facta

from hel_api.views.v1.kiintestotunnukset import API as KiinteistoAPI
from hel_api.views.v1.kaavat import API as KaavaAPI
from hel_api.views.v1.rakennuskiellot import API as RakennuskieltoAPI
from hel_api.views.helpers import format_date

log = logging.getLogger(__name__)


class API(APIView):
    serializer_class = PaikkatietoV1Serializer

    def get(self, request, hankenumero):
        if not hankenumero:
            return HttpResponseBadRequest("Need hankenumero!")

        # Data should reflect the field names defined in Kaavaprojektitiedot excel 'projektitieto tunniste' column
        data = {
            "voimassa_asemakaavat": "",
            "voimassa_olevat_rakennuskiellot": "",
            "maanomistus_kaupunki": "Ei",
            "maanomistus_valtio": "Ei",
            "maanomistus_yksityinen": "Ei",
            "maanomistaja_ulkopaikkakunta": "Ei",
            "haltija_ulkopaikkakunta": "Ei"
        }

        kiinteisto_api = KiinteistoAPI()
        kiinteistotunnukset = kiinteisto_api.get_data(hankenumero)
        for kiinteistotunnus in kiinteistotunnukset["kiinteistotunnukset"]:
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

        kaava_api = KaavaAPI()
        asemakaavat = {kaava["kaavatunnus"]: format_date(kaava["date"]) for kaava in kaava_api.get_data(hankenumero)["kaavat"]}
        asemakaavat_lst = [f"{ak_numero} ({ak_voimassa})" for ak_numero, ak_voimassa in sorted(asemakaavat.items(), reverse=True)]
        data["voimassa_asemakaavat"] = ", ".join(asemakaavat_lst) if asemakaavat_lst else ""

        rakennuskielto_api = RakennuskieltoAPI()
        rakennuskiellot = {rakennuskielto["rakennuskieltotunnus"]: rakennuskielto["selite"] for rakennuskielto in rakennuskielto_api.get_data(hankenumero)["rakennuskiellot"]}
        rakennuskiellot_lst = [f"{rk_numero} ({rk_peruste})" for rk_numero, rk_peruste in sorted(rakennuskiellot.items(), reverse=True)]
        data["voimassa_olevat_rakennuskiellot"] = ", ".join(rakennuskiellot_lst) if rakennuskiellot_lst else ""

        serializer = self.serializer_class(data=data)
        if not serializer.is_valid():
            return HttpResponseServerError("Invalid data!")

        return JsonResponse(data=serializer.validated_data)
