import logging
from pydov.util import location
from .abstract import GeoServer_Reader
from django.core.cache import cache
from django.conf import settings
from hashlib import sha256

log = logging.getLogger(__name__)


class Kiinteistotunnus(GeoServer_Reader):
    use_auth = False
    use_opendata = True
    layername = "hel:Kiinteisto_alue"
    schema = {
        "geometry": "GeometryCollection",
        "geometry_column": "geom",
        "properties": {
            "datanomistaja": "string",
            "id": "int",
            "kiinteisto": "string",
            "kiinteistotunnus": "string",
            "kunta": "string",
            "luontipvm": "date",
            "muokkauspvm": "date",
            "paivitetty_tietopalveluun": "date",
            "rekisterointipvm": "date",
            "ryhma": "string",
            "sijaintialue": "string",
            "yksikko": "string",
        },
        "required": ["id"],
    }

    def get(self, kiinteistotunnus):
        cache_key = f'geoserver_api_kiinteistotunnus_get_{kiinteistotunnus}'
        result = cache.get(cache_key)

        if result is None:
            fields_to_retrieve = self._schema_to_fieldlist()
            num_returned, result = self.query(
                fields_to_retrieve, filter={"kiinteistotunnus": kiinteistotunnus}
            )
            cache.set(cache_key, result, settings.GEOSERVER_CACHE_TIMEOUT)

        return result

    def get_by_geom(self, data, single_result=False):
        _hash = sha256(f'{data}:{single_result}'.encode("utf-8")).hexdigest()
        cache_key = f'geoserver_api_kiinteistotunnus_get_by_geom_{_hash}'
        result = cache.get(cache_key)

        if result is None:
            gml_polygon = self.convert_data(data)
            if not isinstance(gml_polygon, location.GmlObject):
                raise ValueError("Need GmlObject as input!")

            fields_to_retrieve = self._schema_to_fieldlist()
            num_returned, result = self.query(
                fields_to_retrieve,
                filter=gml_polygon,
                limit_results_to=1000,
                return_single_result=single_result,
            )
            cache.set(cache_key, result, settings.GEOSERVER_CACHE_TIMEOUT)

        return result
