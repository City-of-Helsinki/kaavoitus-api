import logging
from pydov.util import location
from .abstract import GeoServer_Reader

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
        gml_polygon = self.convert_data(data)
        if not isinstance(gml_polygon, location.GmlObject):
            raise ValueError("Need GmlObject as input!")

        fields_to_retrieve = self._schema_to_fieldlist()
        num_returned, data = self.query(
            fields_to_retrieve, filter=gml_polygon, return_single_result=single_result
        )

        return data

    def get_by_kaava_id(self, kaava_id):
        fields_to_retrieve = self._schema_to_fieldlist()
        num_returned, data = self.query(
            fields_to_retrieve, filter={"kaavatunnus": kaava_id}
        )

        return data
