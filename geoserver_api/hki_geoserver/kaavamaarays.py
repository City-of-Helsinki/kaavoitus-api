import logging
from pydov.util import location
from .abstract import GeoServer_Reader
from django.core.cache import cache
from django.conf import settings
from hashlib import sha256

log = logging.getLogger(__name__)


class Kaavamaarays(GeoServer_Reader):
    use_auth = False
    layername = "hel:kaavamaarays"
    schema = {
        "geometry": "GeometryCollection",
        "geometry_column": "geom",
        "properties": {
            "angle": "double",
            "asemakaava_uuid_asemakaava": "string",
            "gid": "int",
            "kaavamaarays_uuid": "string",
            "leveys": "string",
            "luokka": "string",
            "maanalainen": "boolean",
            "paivitetty_tietopalveluun": "date",
            "pintaala": "double",
            "rakennusala_uuid_rakennusala": "string",
            "sitova": "boolean",
            "symbolityyppi": "string",
            "teksti": "string",
            "tyyppi": "string",
            "x_scale": "double",
            "y_scale": "double",
            "yhtdatanomistaja": "string",
            "yhtluontipvm": "date",
            "yhtmuokkauspvm": "date",
            "ymparistoalue_uuid_ymparistoalue": "string",
        },
        "required": ["gid", "kaavamaarays_uuid"],
    }

    def get_by_geom(self, data, single_result=False):
        _hash = sha256(f'{data}:{single_result}'.encode("utf-8")).hexdigest()
        cache_key = f'geoserver_api_kaavamaarays_get_by_geom_{_hash}'
        result = cache.get(cache_key)

        if result is None:
            gml_polygon = self.convert_data(data)
            if not isinstance(gml_polygon, location.GmlObject):
                raise ValueError("Need GmlObject as input!")

            fields_to_retrieve = self._schema_to_fieldlist()
            num_returned, result = self.query(
                fields_to_retrieve,
                filter=gml_polygon,
                limit_results_to=10000,
                return_single_result=single_result,
            )
            cache.set(cache_key, result, settings.GEOSERVER_CACHE_TIMEOUT)

        return result
