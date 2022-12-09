import logging
from .abstract import GeoServer_Reader
from django.core.cache import cache
from django.conf import settings

log = logging.getLogger(__name__)


class Maarekisterikiinteisto(GeoServer_Reader):
    use_auth = False
    layername = "hel:Kiinteisto_alue_maarekisterikiinteisto"
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
            "yksikko": "string",
        },
        "required": ["id"],
    }

    def get(self, kiinteistotunnus):
        cache_key = f'geoserver_api_maarekisterikiinteisto_get_{kiinteistotunnus}'
        result = cache.get(cache_key)

        if result is None:
            fields_to_retrieve = self._schema_to_fieldlist()
            num_returned, result = self.query(
                fields_to_retrieve, filter={"kiinteistotunnus": kiinteistotunnus}
            )
            cache.set(cache_key, result, settings.GEOSERVER_CACHE_TIMEOUT)

        return result
