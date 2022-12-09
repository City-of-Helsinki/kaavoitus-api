import logging
from .abstract import GeoServer_Reader
from django.core.cache import cache
from django.conf import settings

log = logging.getLogger(__name__)


class Asemakaava(GeoServer_Reader):
    use_auth = False
    layername = "helsinki:asemakaava"
    use_old_url = True
    schema = {
        "geometry": "GeometryCollection",
        "geometry_column": "geom",
        "properties": {
            "aluesijainti": "string",
            "asemakaava_uuid": "string",
            "gid": "int",
            "hankenumero": "string",
            "hyvaksyja": "string",
            "hyvaksymispvm": "date",
            "kaavalinkki": "string",
            "kaavamaarayskirjasto": "string",
            "kaavanimi1": "string",
            "kaavanimi2": "string",
            "kaavanlaatija": "string",
            "kaavanvaihe": "string",
            "kaavatunnus": "string",
            "kaavatyyppi": "string",
            "kaavatyyppi2": "string",
            "kieli1": "string",
            "kieli2": "string",
            "kuntakoodi": "decimal",
            "lisatietoja": "string",
            "nahtavillaviimpvm": "date",
            "nahtavillealkupvm": "date",
            "paivitetty_tietopalveluun": "date",
            "pintaala": "double",
            "vireilletulopvm": "date",
            "voimaantulopvm": "date",
            "yhtdatanomistaja": "string",
            "yhtluontipvm": "date",
            "yhtmuokkauspvm": "date",
        },
        "required": ["gid", "asemakaava_uuid"],
    }

    def get(self, kaavatunnus):
        cache_key = f'geoserver_api_asemakaava_get_{kaavatunnus}'
        result = cache.get(cache_key)

        if result is None:
            fields_to_retrieve = self._schema_to_fieldlist()
            num_returned, result = self.query(
                fields_to_retrieve, filter={"kaavatunnus": kaavatunnus}
            )
            cache.set(cache_key, result, settings.GEOSERVER_CACHE_TIMEOUT)

        return result

    def get_by_hankenumero(self, hankenumero):
        cache_key = f'geoserver_api_asemakaava_get_by_hankenumero_{hankenumero}'
        result = cache.get(cache_key)

        if result is None:
            fields_to_retrieve = self._schema_to_fieldlist()
            num_returned, result = self.query(
                fields_to_retrieve, filter={"hankenumero": hankenumero}
            )
            cache.set(cache_key, result, settings.GEOSERVER_CACHE_TIMEOUT)

        return result
