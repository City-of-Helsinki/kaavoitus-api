import logging
from .abstract import GeoServer_Reader

log = logging.getLogger(__name__)


class Kaavahanke(GeoServer_Reader):
    use_auth = True
    layername = "helsinki:Hankerajaukset_alue_kaavahanke"
    schema = {
        "geometry": "GeometryCollection",
        "geometry_column": "geom",
        "properties": {
            "tietopalvelu_id": "int",
            "hankenumero": "string",
            "kaavahankkeen_nimi": "string",
            "kaavahankkeen_kuvaus": "string",
            "vastuuhenkilo": "string",
            "vastuuyksikko": "string",
            "muut_vastuuhenkilot": "string",
            "toimintasuunnitelmaan": "string",
            "diaarinumero": "string",
            "kaavanumero": "string",
            "hanketyyppi": "string",
            "kaavaprosessi": "string",
            "maankayttosopimus": "string",
            "kaavavaihe": "string",
            "oas_pvm": "string",
            "asuminen_yhteensa_k_m2": "double",
            "toimitila_yhteensa_k_m2": "double",
            "suunnitteluperiaatteet_suunniteltu_pvm": "string",
            "suunnitteluperiaatteet_hyvaksytty_pvm": "string",
            "luonnos_suunniteltu_pvm": "string",
            "luonnos_hyvaksytty_pvm": "string",
            "ehdotus_suunniteltu_pvm": "string",
            "ehdotus_hyvaksytty_pvm": "string",
            "tarkistettu_ehdotus_suunniteltu_pvm": "string",
            "tarkistettu_ehdotus_hyvaksytty_pvm": "string",
            "hyvaksytty_pvm": "string",
            "hyvaksyja": "string",
            "tavoite_1": "string",
            "tavoite_2": "string",
            "tavoite_3": "string",
            "aineistot_pwssa": "string",
            "luontipvm": "date",
            "muokkauspvm": "date",
            "selostus": "string",
            "datanomistaja": "string",
            "paivitetty_tietopalveluun": "date",
        },
        "required": ["hankenumero"],
    }

    def get(self, pinonro):
        fields_to_retrieve = self._schema_to_fieldlist()
        num_returned, data = self.query(fields_to_retrieve, filter={"pinonro": pinonro})

        return data

    def get_by_hankenumero(self, hankenumero):
        fields_to_retrieve = self._schema_to_fieldlist()
        num_returned, data = self.query(
            fields_to_retrieve, filter={"hankenumero": hankenumero}
        )

        return data
