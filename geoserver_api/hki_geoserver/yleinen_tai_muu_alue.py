import logging
from pydov.util import location
from .abstract import GeoServer_Reader
from django.core.cache import cache
from django.conf import settings
from hashlib import sha256

log = logging.getLogger(__name__)


class YleinenTaiMuuAlue(GeoServer_Reader):
    use_auth = False
    layername = "hel:Yleinen_tai_muu_alue"
    schema = {
        "geometry": "GeometryCollection",
        "geometry_column": "geom",
        "properties": {
            "gid": "int",
            "yleinen_tai_muu_alue_uuid": "string",
            "kayttotarkoitus": "string",
            "tyyppi": "string",
            "maanalainen": "boolean",
            "tehokkuusluku": "double",
            "kaavamerkinta": "string",
            "km2": "double",
            "lisakm2": "double",
            "lisakm2rivita": "boolean",
            "yhteensakm2": "double",
            "kellari": "string",
            "kerrosluku": "string",
            "ullakko": "string",
            "korttelinnumero": "string",
            "knumerokartalle": "boolean",
            "pintaala": "double",
            "lisatietoja": "string",
            "lisakm2kuvaus": "string",
            "yhtluontipvm": "date",
            "yhtmuokkauspvm": "date",
            "yhtdatanomistaja": "string",
            "asemakaava_uuid_asemakaava": "string",
            "paivitetty_tietopalveluun": "date",
        },
        "required": ["gid", "yleinen_tai_muu_alue_uuid"],
    }

    def get_by_geom(self, data, single_result=False):
        _hash = sha256(f'{data}:{single_result}'.encode("utf-8")).hexdigest()
        cache_key = f'geoserver_api_yleinen_tai_muu_alue_get_by_geom_{_hash}'
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
