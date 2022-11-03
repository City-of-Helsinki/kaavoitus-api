import logging
from pydov.util import location
from .abstract import GeoServer_Reader
from django.core.cache import cache
from django.conf import settings
from hashlib import sha256

log = logging.getLogger(__name__)


class Ymparistoalue(GeoServer_Reader):
    use_auth = False
    layername = "hel:ymparistoalue"
    schema = {
        "geometry": "GeometryCollection",
        "geometry_column": "geom",
        "properties": {
            "asemakaava_uuid_asemakaava": "string",
            "gid": "int",
            "paivitetty_tietopalveluun": "date",
            "pintaala": "double",
            "tyyppi": "string",
            "yhtdatanomistaja": "string",
            "yhtluontipvm": "date",
            "yhtmuokkauspvm": "date",
            "ymparistoalue_uuid": "string",
        },
        "required": ["gid", "ymparistoalue_uuid"],
    }

    def get_by_geom(self, data, single_result=False):
        _hash = sha256(f'{data}:{single_result}'.encode("utf-8")).hexdigest()
        cache_key = f'geoserver_api_ymparistoalue_get_by_geom_{_hash}'
        result = cache.get(cache_key)

        if result is None:
            gml_polygon = self.convert_data(data)
            if not isinstance(gml_polygon, location.GmlObject):
                raise ValueError("Need GmlObject as input!")

            fields_to_retrieve = self._schema_to_fieldlist()
            num_returned, result = self.query(
                fields_to_retrieve,
                filter=gml_polygon,
                return_single_result=single_result,
            )
            cache.set(cache_key, result, settings.GEOSERVER_CACHE_TIMEOUT)

        return result
