import logging
from pydov.util import location
from .abstract import GeoServer_Reader
from django.core.cache import cache
from django.conf import settings
from hashlib import sha256

log = logging.getLogger(__name__)


class Asemakaava_voimassa(GeoServer_Reader):
    use_auth = False
    layername = "hel:Kaavahakemisto_alue_kaava_voimassa"
    schema = {
        "geometry": "GeometryCollection",
        "geometry_column": "geom",
        "properties": {
            "alkuperainen": "string",
            "datanomistaja": "string",
            "hyvaksymispvm": "string",
            "id": "int",
            "kaavatunnus": "string",
            "korkeusjarjestelma": "string",
            "lainvoimaisuuspvm": "date",
            "luokka": "string",
            "luontipvm": "date",
            "muokkauspvm": "date",
            "paivitetty_tietopalveluun": "date",
            "pintaala": "decimal",
            "sijaintialue": "string",
            "tyyppi": "string",
            "vahvistamispvm": "date",
            "voimaantulopvm": "date",
        },
        "required": ["id"],
    }

    def get_by_geom(self, data, single_result=False):
        _hash = sha256(f'{data}:{single_result}'.encode("utf-8")).hexdigest()
        cache_key = f'geoserver_api_asemakaava_voimassa_get_by_geom_{_hash}'
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

    def get_by_kaava_id(self, kaava_id):
        cache_key = f'geoserver_api_asemakaava_voimassa_get_by_kaava_id_{kaava_id}'
        result = cache.get(cache_key)

        if result is None:
            fields_to_retrieve = self._schema_to_fieldlist()
            num_returned, result = self.query(
                fields_to_retrieve, filter={"kaavatunnus": kaava_id}
            )
            cache.set(cache_key, result, settings.GEOSERVER_CACHE_TIMEOUT)

        return result
