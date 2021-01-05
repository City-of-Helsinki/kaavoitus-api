import logging
from .abstract import GeoServer_Reader

log = logging.getLogger(__name__)


class Kiinteistotunnus(GeoServer_Reader):
    use_auth = False
    layername = 'avoindata:Kiinteisto_alue'
    schema = {'geometry': 'GeometryCollection',
              'geometry_column': 'geom',
              'properties': {'datanomistaja': 'string',
                             'id': 'int',
                             'kiinteisto': 'string',
                             'kiinteistotunnus': 'string',
                             'kunta': 'string',
                             'luontipvm': 'date',
                             'muokkauspvm': 'date',
                             'paivitetty_tietopalveluun': 'date',
                             'rekisterointipvm': 'date',
                             'ryhma': 'string',
                             'sijaintialue': 'string',
                             'yksikko': 'string'},
              'required': ['id']}

    def get(self, kiinteistotunnus):
        fields_to_retrieve = self._schema_to_fieldlist()
        num_returned, data = self.query(fields_to_retrieve,
                                        filter={'kiinteistotunnus': kiinteistotunnus}
                                        )

        return data
