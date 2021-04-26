import logging
from pydov.util import location
from .abstract import GeoServer_Reader

log = logging.getLogger(__name__)


class Kaavamaarays(GeoServer_Reader):
    use_auth = False
    layername = 'avoindata:kaavamaarays'
    schema = {'geometry': 'GeometryCollection',
              'geometry_column': 'geom',
              'properties': {'angle': 'double',
                             'asemakaava_uuid_asemakaava': 'string',
                             'gid': 'int',
                             'kaavamaarays_uuid': 'string',
                             'leveys': 'string',
                             'luokka': 'string',
                             'maanalainen': 'boolean',
                             'paivitetty_tietopalveluun': 'date',
                             'pintaala': 'double',
                             'rakennusala_uuid_rakennusala': 'string',
                             'sitova': 'boolean',
                             'symbolityyppi': 'string',
                             'teksti': 'string',
                             'tyyppi': 'string',
                             'x_scale': 'double',
                             'y_scale': 'double',
                             'yhtdatanomistaja': 'string',
                             'yhtluontipvm': 'date',
                             'yhtmuokkauspvm': 'date',
                             'ymparistoalue_uuid_ymparistoalue': 'string'},
              'required': ['gid', 'kaavamaarays_uuid']}

    def get(self, gml_polygon):
        if not isinstance(gml_polygon, location.GmlObject):
            raise ValueError("Need GmlObject as input!")

        # Hierarchy to-be-implemented into WFS:
        # kaavanumero/hankenumero/pinonumero/kaavavaihe

        fields_to_retrieve = self._schema_to_fieldlist()
        num_returned, data = self.query(fields_to_retrieve,
                                        filter=gml_polygon,
                                        limit_results_to=1000,
                                        )

        return data

    def get_by_geom(self, gml_polygon):
        if not isinstance(gml_polygon, location.GmlObject):
            raise ValueError("Need GmlObject as input!")

        fields_to_retrieve = self._schema_to_fieldlist()
        num_returned, data = self.query(fields_to_retrieve,
                                        filter=gml_polygon,
                                        limit_results_to=10000,
                                        return_single_result=False,
                                        )

        return data