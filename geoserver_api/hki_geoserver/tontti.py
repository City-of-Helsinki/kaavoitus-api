from pydov.util import location
import copy
import logging
from .abstract import GeoServer_Reader_json

log = logging.getLogger(__name__)


class Tontti(GeoServer_Reader_json):
    use_auth = True
    layername = 'helsinki:Kiinteisto_alue_tontti'
    schema = {'geometry': 'GeometryCollection',
              'geometry_column': 'geom',
              'properties': {'datanomistaja': 'string',
                             'estx_eid': 'int',
                             'id': 'int',
                             'kayttotark_selite': 'string',
                             'kayttotark_tunnus': 'string',
                             'kiinteisto': 'string',
                             'kiinteisto_viiteavain': 'int',
                             'kiinteistotunnus': 'string',
                             'kohdenimi': 'string',
                             'kumoamispvm': 'date',
                             'kunta': 'string',
                             'lisatietoja': 'string',
                             'luontipvm': 'date',
                             'muokkauspvm': 'date',
                             'olotila_selite': 'string',
                             'olotila_tunnus': 'string',
                             'paivitetty_tietopalveluun': 'date',
                             'pintaala': 'decimal',
                             'pintaala_kok': 'decimal',
                             'pintaala_lask': 'decimal',
                             'pintaala_maa': 'decimal',
                             'pintaala_vesi': 'decimal',
                             'rekisterilaji_selite': 'string',
                             'rekisterilaji_tunnus': 'string',
                             'rekisterointipvm': 'date',
                             'ryhma': 'string',
                             'sijaintialue': 'string',
                             'tehokkuusluku': 'string',
                             'yksikko': 'string'},
              'required': ['id']}

    def get(self, kiinteistotunnus):
        fields_to_retrieve = self._schema_to_fieldlist()
        num_returned, data = self.query(fields_to_retrieve,
                                        filter={'kiinteistotunnus': kiinteistotunnus}
                                        )

        return data

    def list_of_neighbours(self, data, neigh_to_skip=[]):
        gml_polygon_in = self.convert_data(data)
        if not isinstance(gml_polygon_in, location.GmlObject):
            raise ValueError("Need GmlObject as input!")

        gml_polygon = copy.copy(gml_polygon_in)
        fields_to_retrieve = self._schema_to_fieldlist()
        num_returned, data = self.query(fields_to_retrieve,
                                        filter=gml_polygon,
                                        return_single_result=False,
                                        limit_results_to=499
                                        )
        out = [tontti['kiinteistotunnus'] for tontti in data if tontti['kiinteistotunnus'] not in neigh_to_skip]

        return out

    def get_by_geom(self, data):
        gml_polygon = self.convert_data(data)
        if not isinstance(gml_polygon, location.GmlObject):
            raise ValueError("Need GmlObject as input!")

        fields_to_retrieve = self._schema_to_fieldlist()
        num_returned, data = self.query(fields_to_retrieve,
                                        filter=gml_polygon,
                                        limit_results_to=1000,
                                        return_single_result=False,
                                        )

        return data
