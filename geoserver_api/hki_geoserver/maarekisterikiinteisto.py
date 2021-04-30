import logging
from .abstract import GeoServer_Reader_json

log = logging.getLogger(__name__)


class Maarekisterikiinteisto(GeoServer_Reader_json):
    use_auth = True
    layername = 'helsinki:Kiinteisto_alue_maarekisterikiinteisto'
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
                             'yksikko': 'string'},
              'required': ['id']}

    def get(self, kiinteistotunnus):
        fields_to_retrieve = self._schema_to_fieldlist()
        num_returned, data = self.query(fields_to_retrieve,
                                        filter={'kiinteistotunnus': kiinteistotunnus}
                                        )

        return data
