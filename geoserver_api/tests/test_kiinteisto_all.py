from django.urls import reverse
from rest_framework.test import APIClient
from unittest.mock import Mock

from geoserver_api.hki_geoserver import Kiinteistotunnus, Tontti, Maarekisterikiinteisto, KiinteistoAlueYleinenAlue, \
    Asemakaava_voimassa, Rakennuskieltoalue_yleiskaava, Rakennuskieltoalue_asemakaava
from geoserver_api.hki_geoserver.abstract.geoserver_reader import GeoServer_Reader


class TestKiinteistoAll:
    client = APIClient()

    def test_user__valid_data(self, f_token1):
        self.client.credentials(HTTP_AUTHORIZATION="Token " + f_token1.key)
        url = reverse(
            "geoserver:kiinteisto-info", kwargs={"version": 1, "kiinteistotunnus": "091-012-0001-0011"}
        )

        reader = GeoServer_Reader
        reader.query = Mock(return_value=(0, {}))

        kt = Kiinteistotunnus
        kt.get = Mock(
            return_value={
                "datanomistaja": "Helsinki",
                "id": 10001,
                "kiinteisto": "91-12-1-11",
                "kiinteistotunnus": "091-012-0001-0011",
                "kunta": "091",
                "luontipvm": "2021-05-23",
                "muokkauspvm": "2021-05-23",
                "paivitetty_tietopalveluun": "2024-01-13",
                "rekisterointipvm": "2023-12-11",
                "ryhma": "0001",
                "sijaintialue": "312",
                "yksikko": "0310",
                "geom": [
                    {
                        "type": "Feature",
                        "geometry": {
                            "type": "Polygon",
                            "coordinates": [
                                [
                                    [24.9320125579834, 60.17221176544357],
                                    [24.933841824531555, 60.17221176544357],
                                    [24.933841824531555, 60.17283879431961],
                                    [24.9320125579834, 60.17283879431961],
                                    [24.9320125579834, 60.17221176544357],
                                ]
                            ],
                        },
                        "properties": {"id": "Hankerajaukset_alue_kaavahanke.001"},
                    }
                ],
            }
        )

        t = Tontti
        t.get = Mock(
            return_value={
                "datanomistaja": "Helsinki",
                "estx_eid": 10001,
                "id": "Tontti.2",
                "kayttotark_selite": "qwert",
                "kayttotark_tunnus": "A",
                "kiinteisto": "91-12-1-11",
                "kiinteisto_viiteavain": 1111,
                "kiinteistotunnus": "091-012-0001-0011",
                "kohdenimi": "PTY_Tontti",
                "kumoamispvm": "2023-09-17",
                "kunta": "Helsinki",
                "lisatietoja": "amsjg",
                "luontipvm": "2021-11-19",
                "muokkauspvm": "2021-12-11",
                "olotila_selite": "Voimassa",
                "olotila_tunnus": "1",
                "paivitetty_tietopalveluun": "2024-01-11",
                "pintaala": 1602.219251,
                "pintaala_kok": 301.291022,
                "pintaala_lask": 391.012852,
                "pintaala_maa": 792.129842,
                "pintaala_vesi": 118.12929,
                "rekisterilaji_selite": "jasosj",
                "rekisterilaji_tunnus": "T",
                "rekisterointipvm": "2023-12-03",
                "ryhma": "0001",
                "sijaintialue": "0003",
                "tehokkuusluku": "1234",
                "yksikko": "0005",
                "geom": [
                    {
                        "type": "Feature",
                        "geometry": {
                            "type": "Polygon",
                            "coordinates": [
                                [
                                    [24.9320125579834, 60.17221176544357],
                                    [24.933841824531555, 60.17221176544357],
                                    [24.933841824531555, 60.17283879431961],
                                    [24.9320125579834, 60.17283879431961],
                                    [24.9320125579834, 60.17221176544357],
                                ]
                            ],
                        },
                        "properties": {"id": "Hankerajaukset_alue_kaavahanke.001"},
                    }
                ],
            }
        )

        mr = Maarekisterikiinteisto
        mr.get = Mock(
            return_value={
                "datanomistaja": "Helsinki",
                "estx_eid": 10002,
                "id": "Alue.091",
                "kayttotark_selite": "asdgkj",
                "kayttotark_tunnus": "B",
                "kiinteisto": "91-12-1-11",
                "kiinteisto_viiteavain": 91,
                "kiinteistotunnus": "091-012-0001-0011",
                "kohdenimi": "asdjs",
                "kumoamispvm": "2023-11-11",
                "kunta": "Helsinki",
                "lisatietoja": "amsdi",
                "luontipvm": "2020-11-12",
                "muokkauspvm": "2022-11-12",
                "olotila_selite": "Voimassa",
                "olotila_tunnus": "2",
                "paivitetty_tietopalveluun": "2023-12-12",
                "pintaala": 1012.12491,
                "pintaala_kok": 123.23602,
                "pintaala_lask": 129.34692,
                "pintaala_maa": 701.12492,
                "pintaala_vesi": 32.61092,
                "rekisterilaji_selite": "asdgh1",
                "rekisterilaji_tunnus": "M",
                "rekisterointipvm": "2024-11-12",
                "ryhma": "0001",
                "sijaintialue": "0012",
                "yksikko": "0002",
            }
        )

        #  TODO: Fill mock data

        kaya = KiinteistoAlueYleinenAlue
        kaya.get = Mock(
            return_value={}
        )

        akv = Asemakaava_voimassa
        akv.get_by_geom = Mock(
            return_value={}
        )

        rkay = Rakennuskieltoalue_yleiskaava
        rkay.get_by_geom = Mock(
            return_value={}
        )

        rkaa = Rakennuskieltoalue_asemakaava
        rkaa.get_by_geom = Mock(
            return_value={}
        )

        response = self.client.get(url)
        print(f'response: {response}')

        assert response is not None

