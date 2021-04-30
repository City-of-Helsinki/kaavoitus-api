import logging
from pydov.util import location
from .abstract import GeoServer_Reader_json

log = logging.getLogger(__name__)


class YleinenTaiMuuAlue(GeoServer_Reader_json):
    use_auth = False
    layername = 'avoindata:yleinen_tai_muu_alue'
    schema = {'geometry': 'GeometryCollection',
              'geometry_column': 'geom',
              'properties': {
                'gid': 'int',
                'yleinen_tai_muu_alue_uuid': 'string',
                'kayttotarkoitus': 'string',
                'tyyppi': 'string',
                'maanalainen': 'boolean',
                'tehokkuusluku': 'double',
                'kaavamerkinta': 'string',
                'km2': 'double',
                'lisakm2': 'double',
                'lisakm2rivita': 'boolean',
                'yhteensakm2': 'double',
                'kellari': 'string',
                'kerrosluku': 'string',
                'ullakko': 'string',
                'korttelinnumero': 'string',
                'knumerokartalle': 'boolean',
                'pintaala': 'double',
                'lisatietoja': 'string',
                'lisakm2kuvaus': 'string',
                'yhtluontipvm': 'date',
                'yhtmuokkauspvm': 'date',
                'yhtdatanomistaja': 'string',
                'asemakaava_uuid_asemakaava': 'string',
                'paivitetty_tietopalveluun': 'date',
              },
              'required': ['gid', 'yleinen_tai_muu_alue_uuid']}

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
