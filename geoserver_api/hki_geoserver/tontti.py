from pydov.util import location
import copy
import logging
from .abstract import GeoServer_Reader
from django.core.cache import cache
from django.conf import settings
from hashlib import sha256

log = logging.getLogger(__name__)


class Tontti(GeoServer_Reader):
    use_auth = False
    layername = "hel:Kiinteisto_alue_tontti"
    schema = {
        "geometry": "GeometryCollection",
        "geometry_column": "geom",
        "properties": {
            "datanomistaja": "string",
            "estx_eid": "int",
            "id": "int",
            "kayttotark_selite": "string",
            "kayttotark_tunnus": "string",
            "kiinteisto": "string",
            "kiinteisto_viiteavain": "int",
            "kiinteistotunnus": "string",
            "kohdenimi": "string",
            "kumoamispvm": "date",
            "kunta": "string",
            "lisatietoja": "string",
            "luontipvm": "date",
            "muokkauspvm": "date",
            "olotila_selite": "string",
            "olotila_tunnus": "string",
            "paivitetty_tietopalveluun": "date",
            "pintaala": "decimal",
            "pintaala_kok": "decimal",
            "pintaala_lask": "decimal",
            "pintaala_maa": "decimal",
            "pintaala_vesi": "decimal",
            "rekisterilaji_selite": "string",
            "rekisterilaji_tunnus": "string",
            "rekisterointipvm": "date",
            "ryhma": "string",
            "sijaintialue": "string",
            "tehokkuusluku": "string",
            "yksikko": "string",
        },
        "required": ["id"],
    }

    def get(self, kiinteistotunnus):
        cache_key = f'geoserver_api_tontti_get_{kiinteistotunnus}'
        result = cache.get(cache_key)

        if result is None:
            fields_to_retrieve = self._schema_to_fieldlist()
            num_returned, result = self.query(
                fields_to_retrieve, filter={"kiinteistotunnus": kiinteistotunnus}
            )
            cache.set(cache_key, result, settings.GEOSERVER_CACHE_TIMEOUT)

        return result

    def list_of_neighbours(self, data, neigh_to_skip=[]):
        _hash = sha256(f'{data}'.encode("utf-8")).hexdigest()
        cache_key = f'geoserver_api_tontti_list_of_neighbours_{_hash}'
        result = cache.get(cache_key)

        if result is None:
            gml_polygon_in = self.convert_data(data)
            if not isinstance(gml_polygon_in, location.GmlObject):
                raise ValueError("Need GmlObject as input!")

            gml_polygon = copy.copy(gml_polygon_in)
            fields_to_retrieve = self._schema_to_fieldlist()
            num_returned, result = self.query(
                fields_to_retrieve,
                filter=gml_polygon,
                return_single_result=False,
            )
            cache.set(cache_key, result, settings.GEOSERVER_CACHE_TIMEOUT)

        out = [
            tontti["kiinteistotunnus"]
            for tontti in result
            if tontti["kiinteistotunnus"] not in neigh_to_skip
        ]

        return out

    def get_by_geom(self, data, single_result=False):
        _hash = sha256(f'{data}:{single_result}'.encode("utf-8")).hexdigest()
        cache_key = f'geoserver_api_tontti_get_by_geom_{_hash}'
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
