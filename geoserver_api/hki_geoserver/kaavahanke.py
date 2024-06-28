import logging
from .abstract import GeoServer_Reader
from django.core.cache import cache
from django.conf import settings

log = logging.getLogger(__name__)


class Kaavahanke(GeoServer_Reader):
    use_auth = False
    layername = "hel:asemakaava"
    schema = {
        "geometry": "GeometryCollection",
        "geometry_column": "geom",
        "properties": {
            "hankenumero": "string",
            "kaavanimi_fin": "string",
            "kaavatyyppi_tarkennus": "string",
            "diaarinumero": "string",
            "kaavatunnus": "string",
            "kaavatyyppi": "string",
            "kaavavaihe": "string",
            "hyvaksymispvm": "string",
            "hyvaksyja": "string",
            "yhtluontipvm": "date",
            "yhtmuokkauspvm": "date",
            "yhtdatanomistaja": "string",
            "pintaala": "double",
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
