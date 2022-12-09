from pydov.util import location
from .abstract import GeoServer_Reader
from django.core.cache import cache
from django.conf import settings
from hashlib import sha256


class Rakennuskieltoalue_asemakaava(GeoServer_Reader):
    use_auth = False
    layername = "hel:Rakennuskieltoalue_asemakaavan_laatimiseksi"
    schema = {
        "geometry": "GeometryCollection",
        "geometry_column": "geom",
        "properties": {
            "antaja_selite": "string",
            "antaja_tunnus": "string",
            "datanomistaja": "string",
            "id": "int",
            "kunta": "string",
            "laatu_selite": "string",
            "laatu_tunnus": "string",
            "luontipvm": "date",
            "muokkauspvm": "date",
            "paatospvm": "date",
            "paattymispvm": "date",
            "paivitetty_tietopalveluun": "date",
            "rakennuskieltotunnus": "string",
            "tyyppi": "string",
            "voimaantulopvm": "date",
        },
        "required": ["id"],
    }

    def get_by_geom(self, data, single_result=False):
        _hash = sha256(f'{data}:{single_result}'.encode("utf-8")).hexdigest()
        cache_key = f'geoserver_api_rakennuskieltoalue_asemakaava_get_by_geom_{_hash}'
        result = cache.get(cache_key)

        if result is None:
            gml_polygon = self.convert_data(data)
            if not isinstance(gml_polygon, location.GmlObject):
                raise ValueError("Need GmlObject as input!")

            fields_to_retrieve = self._schema_to_fieldlist()
            num_returned, result = self.query(
                fields_to_retrieve, filter=gml_polygon, return_single_result=single_result
            )
            cache.set(cache_key, result, settings.GEOSERVER_CACHE_TIMEOUT)

        return result
