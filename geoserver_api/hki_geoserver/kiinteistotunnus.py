import logging
from pydov.util import location
from .abstract import GeoServer_Reader

log = logging.getLogger(__name__)


class Kiinteistotunnus(GeoServer_Reader):
    use_auth = False
    layername = "avoindata:Kiinteisto_alue"
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
        fields_to_retrieve = self._schema_to_fieldlist()
        num_returned, data = self.query(
            fields_to_retrieve, filter={"kiinteistotunnus": kiinteistotunnus}
        )

        return data

    def get_by_geom(self, data):
        gml_polygon = self.convert_data(data)
        if not isinstance(gml_polygon, location.GmlObject):
            raise ValueError("Need GmlObject as input!")

        fields_to_retrieve = self._schema_to_fieldlist()
        num_returned, data = self.query(
            fields_to_retrieve,
            filter=gml_polygon,
            limit_results_to=1000,
            return_single_result=False,
        )

        return data
