import logging
from .abstract import GeoServer_Reader

log = logging.getLogger(__name__)


class Korttelialue(GeoServer_Reader):
    use_auth = False
    layername = 'avoindata:korttelialue'
    schema = {'geometry': 'GeometryCollection',
              'geometry_column': 'geom',
              'properties': {'asemakaava_uuid_asemakaava': 'string',
                             'gid': 'int',
                             'kaavamerkinta': 'string',
                             'kayttotarkoitus': 'string',
                             'kellari': 'string',
                             'kerrosluku': 'string',
                             'km2': 'double',
                             'knumerokartalle': 'boolean',
                             'korttelialue_uuid': 'string',
                             'korttelinnumero': 'string',
                             'lisakm2': 'double',
                             'lisakm2kuvaus': 'string',
                             'lisakm2rivita': 'boolean',
                             'lisatietoja': 'string',
                             'maanalainen': 'boolean',
                             'paivitetty_tietopalveluun': 'date',
                             'pintaala': 'double',
                             'tehokkuusluku': 'double',
                             'tyyppi': 'string',
                             'ullakko': 'string',
                             'yhtdatanomistaja': 'string',
                             'yhteensakm2': 'double',
                             'yhtluontipvm': 'date',
                             'yhtmuokkauspvm': 'date'},
              'required': ['gid', 'korttelialue_uuid']}

    def get(self, korttelinnumero):
        fields_to_retrieve = self._schema_to_fieldlist()
        num_returned, data = self.query(fields_to_retrieve,
                                        filter={'korttelinnumero': korttelinnumero}
                                        )

        return data
