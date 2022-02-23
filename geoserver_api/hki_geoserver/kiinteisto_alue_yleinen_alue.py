import logging
from pydov.util import location
from .abstract import GeoServer_Reader

log = logging.getLogger(__name__)


class KiinteistoAlueYleinenAlue(GeoServer_Reader):
    use_auth = True
    layername = "hel:Kiinteisto_alue_yleinen_alue"
    schema = {
        "geometry": "GeometryCollection",
        "geometry_column": "geom",
        "properties": {
            "id": "int",
            "kohdenimi": "string",
            "kiinteistotunnus": "string",
            "kiinteisto_viiteavain": "int",
            "kiinteisto": "string",
            "kunta": "string",
            "sijaintialue": "string",
            "ryhma": "string",
            "yksikko": "string",
            "pintaala": "double",
            "pintaala_kok": "double",
            "pintaala_lask": "double",
            "pintaala_maa": "double",
            "pintaala_vesi": "double",
            "rekisterointipvm": "date",
            "kumoamispvm": "date",
            "rekisterilaji_tunnus": "string",
            "rekisterilaji_selite": "string",
            "kayttotark_tunnus": "string",
            "kayttotark_selite": "string",
            "olotila_tunnus": "string",
            "olotila_selite": "string",
            "lisatietoja": "string",
            "estx_eid": "int",
            "luontipvm": "date",
            "muokkauspvm": "date",
            "datanomistaja": "string",
            "paivitetty_tietopalveluun": "date",
        },
        "required": ["id"],
    }

    def get(self, kiinteistotunnus):
        fields_to_retrieve = self._schema_to_fieldlist()
        num_returned, data = self.query(
            fields_to_retrieve, filter={"kiinteistotunnus": kiinteistotunnus}
        )

        return data

    def get_by_geom(self, data, single_result=False):
        gml_polygon = self.convert_data(data)
        if not isinstance(gml_polygon, location.GmlObject):
            raise ValueError("Need GmlObject as input!")

        fields_to_retrieve = self._schema_to_fieldlist()
        num_returned, data = self.query(
            fields_to_retrieve,
            filter=gml_polygon,
            limit_results_to=1000,
            return_single_result=single_result,
        )

        return data
