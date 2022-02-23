import logging
from .abstract import GeoServer_Reader

log = logging.getLogger(__name__)


class Asemakaava(GeoServer_Reader):
    use_auth = True
    layername = "hel:asemakaava"
    schema = {
        "geometry": "GeometryCollection",
        "geometry_column": "geom",
        "properties": {
            "aluesijainti": "string",
            "asemakaava_uuid": "string",
            "gid": "int",
            "hankenumero": "string",
            "hyvaksyja": "string",
            "hyvaksymispvm": "date",
            "kaavalinkki": "string",
            "kaavamaarayskirjasto": "string",
            "kaavanimi1": "string",
            "kaavanimi2": "string",
            "kaavanlaatija": "string",
            "kaavanvaihe": "string",
            "kaavatunnus": "string",
            "kaavatyyppi": "string",
            "kaavatyyppi2": "string",
            "kieli1": "string",
            "kieli2": "string",
            "kuntakoodi": "decimal",
            "lisatietoja": "string",
            "nahtavillaviimpvm": "date",
            "nahtavillealkupvm": "date",
            "paivitetty_tietopalveluun": "date",
            "pintaala": "double",
            "vireilletulopvm": "date",
            "voimaantulopvm": "date",
            "yhtdatanomistaja": "string",
            "yhtluontipvm": "date",
            "yhtmuokkauspvm": "date",
        },
        "required": ["gid", "asemakaava_uuid"],
    }

    def get(self, kaavatunnus):
        fields_to_retrieve = self._schema_to_fieldlist()
        num_returned, data = self.query(
            fields_to_retrieve, filter={"kaavatunnus": kaavatunnus}
        )

        return data

    def get_by_hankenumero(self, hankenumero):
        fields_to_retrieve = self._schema_to_fieldlist()
        num_returned, data = self.query(
            fields_to_retrieve, filter={"hankenumero": hankenumero}
        )

        return data
