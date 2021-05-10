import logging
from pydov.util import location
from .abstract import GeoServer_Reader

log = logging.getLogger(__name__)


class Ymparistoalue(GeoServer_Reader):
    use_auth = False
    layername = "avoindata:ymparistoalue"
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
        gml_polygon = self.convert_data(data)
        if not isinstance(gml_polygon, location.GmlObject):
            raise ValueError("Need GmlObject as input!")

        fields_to_retrieve = self._schema_to_fieldlist()
        num_returned, data = self.query(
            fields_to_retrieve,
            filter=gml_polygon,
            return_single_result=single_result,
        )

        return data
