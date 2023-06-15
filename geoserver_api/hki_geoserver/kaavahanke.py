import logging
from .abstract import GeoServer_Reader
from django.core.cache import cache
from django.conf import settings

log = logging.getLogger(__name__)


class Kaavahanke(GeoServer_Reader):
    use_auth = False
    layername = "hel:Hankerajaukset_alue_kaavahanke"
    schema = {
        "geometry": "GeometryCollection",
        "geometry_column": "geom",
        "properties": {
            "tietopalvelu_id": "int",
            "hankenumero": "string",
            "kaavahankkeen_nimi": "string",
            "kaavahankkeen_kuvaus": "string",
            "vastuuhenkilo": "string",
            "vastuuyksikko": "string",
            "muut_vastuuhenkilot": "string",
            "toimintasuunnitelmaan": "string",
            "diaarinumero": "string",
            "kaavanumero": "string",
            "hanketyyppi": "string",
            "kaavaprosessi": "string",
            "maankayttosopimus": "string",
            "kaavavaihe": "string",
            "oas_pvm": "string",
            "asuminen_yhteensa_k_m2": "double",
            "toimitila_yhteensa_k_m2": "double",
            "suunnitteluperiaatteet_suunniteltu_pvm": "string",
            "suunnitteluperiaatteet_hyvaksytty_pvm": "string",
            "luonnos_suunniteltu_pvm": "string",
            "luonnos_hyvaksytty_pvm": "string",
            "ehdotus_suunniteltu_pvm": "string",
            "ehdotus_hyvaksytty_pvm": "string",
            "tarkistettu_ehdotus_suunniteltu_pvm": "string",
            "tarkistettu_ehdotus_hyvaksytty_pvm": "string",
            "hyvaksytty_pvm": "string",
            "hyvaksyja": "string",
            "tavoite_1": "string",
            "tavoite_2": "string",
            "tavoite_3": "string",
            "aineistot_pwssa": "string",
            "luontipvm": "date",
            "muokkauspvm": "date",
            "selostus": "string",
            "datanomistaja": "string",
            "paivitetty_tietopalveluun": "date",
            "pinta_ala": "double",
        },
        "required": ["hankenumero"],
    }

    def get(self, pinonro):
        cache_key = f'geoserver_api_kaavahanke_get_{pinonro}'
        result = cache.get(cache_key)

        if result is None:
            fields_to_retrieve = self._schema_to_fieldlist()
            num_returned, result = self.query(fields_to_retrieve, filter={"pinonro": pinonro})
            cache.set(cache_key, result, settings.GEOSERVER_CACHE_TIMEOUT)

        return result

    def get_by_hankenumero(self, hankenumero):
        cache_key = f'geoserver_api_kaavahanke_get_by_hankenumero_{hankenumero}'
        result = cache.get(cache_key)

        if result is None:
            fields_to_retrieve = self._schema_to_fieldlist()
            num_returned, result = self.query(
                fields_to_retrieve, filter={"hankenumero": hankenumero}
            )
            cache.set(cache_key, result, settings.GEOSERVER_CACHE_TIMEOUT)

        return result
