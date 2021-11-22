from django.urls import reverse
from rest_framework.test import APIClient
from unittest.mock import Mock

from geoserver_api.hki_geoserver.rakennusala import Rakennusala
from geoserver_api.hki_geoserver.yleinen_tai_muu_alue import YleinenTaiMuuAlue
from geoserver_api.hki_geoserver.korttelialue import Korttelialue
from geoserver_api.hki_geoserver.kaavamaarays import Kaavamaarays
from geoserver_api.hki_geoserver.tontti import Tontti
from geoserver_api.hki_geoserver.asemakaava import Asemakaava
from geoserver_api.hki_geoserver.kaavahanke import Kaavahanke
from geoserver_api.hki_geoserver.abstract.geoserver_reader import GeoServer_Reader


class TestSuunnittelualue:
    client = APIClient()

    def test_user__valid_data(self, f_token1):
        self.client.credentials(HTTP_AUTHORIZATION="Token " + f_token1.key)
        url = reverse(
            "geoserver:suunnittelualue", kwargs={"version": 1, "hankenumero": 1}
        )

        reader = GeoServer_Reader
        reader.query = Mock(return_value=(0, {}))

        kh = Kaavahanke
        kh.get_by_hankenumero = Mock(
            return_value={
                "tietopalvelu_id": "001",
                "hankenumero": "0001_1",
                "kaavahankkeen_nimi": "Testinimi",
                "kaavahankkeen_kuvaus": "Testikuvaus",
                "vastuuhenkilo": "Testaaja1",
                "vastuuyksikko": "Testaus",
                "muut_vastuuhenkilot": "Testaus/Testaaja2",
                "toimintasuunnitelmaan": "Kyllä",
                "diaarinumero": "HEL 2021-000001",
                "kaavanumero": "00001",
                "hanketyyppi": "asemakaava",
                "kaavaprosessi": "XL",
                "maankayttosopimus": None,
                "kaavavaihe": "Testausvaihe",
                "oas_pvm": "01.01.2021",
                "asuminen_yhteensa_k_m2": 12345,
                "toimitila_yhteensa_k_m2": 9876,
                "suunnitteluperiaatteet_suunniteltu_pvm": None,
                "suunnitteluperiaatteet_hyvaksytty_pvm": None,
                "luonnos_suunniteltu_pvm": "01.01.2020",
                "luonnos_hyvaksytty_pvm": "01.02.2020",
                "ehdotus_suunniteltu_pvm": "01.03.2020",
                "ehdotus_hyvaksytty_pvm": "01.04.2020",
                "tarkistettu_ehdotus_suunniteltu_pvm": "01.05.2020",
                "tarkistettu_ehdotus_hyvaksytty_pvm": None,
                "hyvaksytty_pvm": None,
                "hyvaksyja": None,
                "tavoite_1": "Testataan 1",
                "tavoite_2": "Testataan 2",
                "tavoite_3": "Testataa3 3",
                "aineistot_pwssa": "dev://null",
                "luontipvm": "2020-04-01",
                "muokkauspvm": "2020-05-01",
                "selostus": None,
                "datanomistaja": "Helsinki/MAKA",
                "paivitetty_tietopalveluun": "2021-02-01",
                "id": "Hankerajaukset_alue_kaavahanke.001",
                "srs": "urn:ogc:def:crs:EPSG::3879",
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

        ak = Asemakaava
        ak.get_by_hankenumero = Mock(
            return_value={
                "gid": 1,
                "asemakaava_uuid": "11111111-2222-3333-4444-555555555555",
                "kaavatunnus": "00001",
                "hankenumero": "0001_1",
                "kieli1": "fi-FI",
                "kieli2": "sv-FI",
                "kaavanimi1": "Testinimi1",
                "kaavanimi2": None,
                "kaavanlaatija": "Testaaja3",
                "hyvaksyja": None,
                "vireilletulopvm": "2020-04-01",
                "hyvaksymispvm": "2020-04-01",
                "voimaantulopvm": "2020-04-01",
                "kuntakoodi": 91,
                "kaavanvaihe": "vireilletullut",
                "kaavatyyppi": "Asemakaava",
                "kaavatyyppi2": None,
                "aluesijainti": "voimaantulosijainti",
                "nahtavillealkupvm": "2020-04-01",
                "nahtavillaviimpvm": "2020-04-01",
                "kaavamaarayskirjasto": "Testikirjasto",
                "kaavalinkki": None,
                "pintaala": 876543.210000,
                "lisatietoja": None,
                "yhtluontipvm": "2020-04-01",
                "yhtmuokkauspvm": "2020-05-01",
                "yhtdatanomistaja": "Helsinki/Kymp/Maka/Aska",
                "paivitetty_tietopalveluun": None,
                "id": "asemakaava.01",
                "srs": "urn:ogc:def:crs:EPSG::3879",
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
                        "properties": {"id": "asemakaava.01"},
                    }
                ],
            }
        )

        t = Tontti
        t.get_by_geom = Mock(
            return_value=[
                {
                    "id": "Kiinteisto_alue_tontti.00001",
                    "kohdenimi": "PTY_KiinteistoAlue",
                    "kiinteistotunnus": "01020304050607",
                    "kiinteisto_viiteavain": 1111,
                    "kiinteisto": "01-02-03-0",
                    "kunta": "091",
                    "sijaintialue": "031",
                    "ryhma": "0001",
                    "yksikko": "0002",
                    "pintaala": 1234.56789,
                    "pintaala_kok": 1235,
                    "pintaala_lask": None,
                    "pintaala_maa": 1235,
                    "pintaala_vesi": 0,
                    "tehokkuusluku": 1234,
                    "rekisterointipvm": "1960-01-01",
                    "kumoamispvm": None,
                    "rekisterilaji_tunnus": "T",
                    "rekisterilaji_selite": "Tontti",
                    "kayttotark_tunnus": "A",
                    "kayttotark_selite": "ASUNTO",
                    "olotila_tunnus": "1",
                    "olotila_selite": "Voimassa",
                    "lisatietoja": None,
                    "estx_eid": 10001,
                    "luontipvm": "2010-12-01",
                    "muokkauspvm": "2011-06-01",
                    "datanomistaja": "Helsinki/Kami",
                    "paivitetty_tietopalveluun": "2021-05-01",
                    "srs": "urn:ogc:def:crs:EPSG::3879",
                    "geom": [
                        {
                            "type": "Feature",
                            "geometry": {
                                "type": "MultiPolygon",
                                "coordinates": [
                                    [
                                        [
                                            [24.9320125579834, 60.17221176544357],
                                            [24.933841824531555, 60.17221176544357],
                                            [24.933841824531555, 60.17283879431961],
                                            [24.9320125579834, 60.17283879431961],
                                            [24.9320125579834, 60.17221176544357],
                                        ]
                                    ]
                                ],
                            },
                            "properties": {"id": "Kiinteisto_alue_tontti.00001"},
                        }
                    ],
                }
            ]
        )

        km = Kaavamaarays
        km.get_by_geom = Mock(
            return_value=[
                {
                    "gid": 10001,
                    "kaavamaarays_uuid": "aaaaaaaa-bbbb-cccc-dddd-ffffffffffff",
                    "tyyppi": "Alueenosan raja",
                    "luokka": "MuuAsemakaavaViiva",
                    "teksti": None,
                    "symbolityyppi": None,
                    "maanalainen": True,
                    "leveys": None,
                    "sitova": False,
                    "pintaala": 2222.123456,
                    "yhtluontipvm": "2020-04-01",
                    "yhtmuokkauspvm": "2020-05-01",
                    "yhtdatanomistaja": None,
                    "angle": None,
                    "x_scale": None,
                    "y_scale": None,
                    "asemakaava_uuid_asemakaava": "11111111-2222-3333-4444-555555555555",
                    "rakennusala_uuid_rakennusala": None,
                    "ymparistoalue_uuid_ymparistoalue": None,
                    "paivitetty_tietopalveluun": None,
                    "id": "kaavamaarays.aaaaaaaa-bbbb-cccc-dddd-ffffffffffff",
                    "srs": "urn:ogc:def:crs:EPSG::3879",
                    "geom": [
                        {
                            "type": "Feature",
                            "geometry": {
                                "type": "MultiLineString",
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
                            "properties": {
                                "id": "kaavamaarays.aaaaaaaa-bbbb-cccc-dddd-ffffffffffff"
                            },
                        }
                    ],
                }
            ]
        )

        ka = Korttelialue
        ka.get_by_geom = Mock(
            return_value=[
                {
                    "gid": 123,
                    "korttelialue_uuid": "bbbbbbbb-cccc-dddd-eeee-ffffffffffff",
                    "kayttotarkoitus": "Kortteli tai korttelinosa",
                    "tyyppi": "LPA",
                    "maanalainen": False,
                    "tehokkuusluku": None,
                    "kaavamerkinta": "LPA",
                    "km2": None,
                    "lisakm2": None,
                    "lisakm2rivita": False,
                    "yhteensakm2": None,
                    "kellari": None,
                    "kerrosluku": None,
                    "ullakko": None,
                    "korttelinnumero": "31165",
                    "knumerokartalle": False,
                    "pintaala": 3451.376978,
                    "lisatietoja": None,
                    "lisakm2kuvaus": None,
                    "yhtluontipvm": "2020-04-01",
                    "yhtmuokkauspvm": "2020-05-01",
                    "yhtdatanomistaja": "Helsinki/Kymp/Maka/Aska",
                    "asemakaava_uuid_asemakaava": "11111111-2222-3333-4444-555555555555",
                    "paivitetty_tietopalveluun": None,
                    "id": "korttelialue.bbbbbbbb-cccc-dddd-eeee-ffffffffffff",
                    "srs": "urn:ogc:def:crs:EPSG::3879",
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
                            "properties": {
                                "id": "korttelialue.bbbbbbbb-cccc-dddd-eeee-ffffffffffff"
                            },
                        }
                    ],
                }
            ]
        )

        ya = YleinenTaiMuuAlue
        ya.get_by_geom = Mock(
            return_value=[
                {
                    "gid": 234,
                    "yleinen_tai_muu_alue_uuid": "cccccccc-dddd-eeee-ffff-gggggggggggg",
                    "kayttotarkoitus": "Vesialue",
                    "tyyppi": "W - Vesialue",
                    "maanalainen": False,
                    "tehokkuusluku": None,
                    "kaavamerkinta": "W",
                    "km2": None,
                    "lisakm2": None,
                    "lisakm2rivita": False,
                    "yhteensakm2": None,
                    "kellari": None,
                    "kerrosluku": None,
                    "ullakko": None,
                    "korttelinnumero": None,
                    "knumerokartalle": False,
                    "pintaala": 456.789012,
                    "lisatietoja": None,
                    "lisakm2kuvaus": None,
                    "yhtluontipvm": "2019-01-01",
                    "yhtmuokkauspvm": "2019-02-01",
                    "yhtdatanomistaja": "Helsinki/KMO",
                    "asemakaava_uuid_asemakaava": "11111111-2222-3333-4444-555555555555",
                    "paivitetty_tietopalveluun": None,
                    "id": "yleinen_tai_muu_alue.cccccccc-dddd-eeee-ffff-gggggggggggg",
                    "srs": "urn:ogc:def:crs:EPSG::3879",
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
                            "properties": {
                                "id": "yleinen_tai_muu_alue.cccccccc-dddd-eeee-ffff-gggggggggggg"
                            },
                        }
                    ],
                }
            ]
        )

        ra = Rakennusala
        ra.get_by_geom = Mock(
            return_value=[
                {
                    "gid": 345,
                    "rakennusala_uuid": "dddddddd-eeee-ffff-gggg-hhhhhhhhhhhh",
                    "tyyppi": "rakennusala",
                    "maanalainen": False,
                    "kaavamerkinta": "s",
                    "km2": None,
                    "lisakm2": None,
                    "lisakm2rivita": False,
                    "kellari": None,
                    "kerrosluku": None,
                    "ullakko": None,
                    "varisavy": "0",
                    "sitova": False,
                    "pintaala": 50.987654,
                    "lisatietoja": None,
                    "lisakm2kuvaus": None,
                    "yhtluontipvm": "2019-01-02",
                    "yhtmuokkauspvm": "2019-02-02",
                    "yhtdatanomistaja": "Helsinki/KMO",
                    "asemakaava_uuid_asemakaava": "11111111-2222-3333-4444-555555555555",
                    "ra_tyyppi_uuid_ra_tyyppi": "11111111-aaaa-2222-bbbb-333333333333",
                    "paivitetty_tietopalveluun": None,
                    "id": "rakennusala.dddddddd-eeee-ffff-gggg-hhhhhhhhhhhh",
                    "srs": "urn:ogc:def:crs:EPSG::3879",
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
                            "properties": {
                                "id": "rakennusala.dddddddd-eeee-ffff-gggg-hhhhhhhhhhhh"
                            },
                        }
                    ],
                }
            ]
        )

        response = self.client.get(url)

        assert response.status_code == 200
        assert response.json() == {
            "aluevarausten_pinta_alat_yht": "3908.16599",
            "keskimaarainen_tonttitehokkuus": "1234.0",
            "maanalaisten_tilojen_pinta_ala_yht": "2222.123456",
            "pinta_alan_muutokset_yht": "0.0",
            "suojellut_rakennukset_ala_yht": "50.987654",
            "suojellut_rakennukset_maara_yht": "1",
            "suunnittelualueen_pinta_ala": "876543.21",
            "suunnittelualueen_rajaus": [
                {
                    "geometry": {
                        "coordinates": [
                            [
                                [24.9320125579834, 60.17221176544357],
                                [24.933841824531555, 60.17221176544357],
                                [24.933841824531555, 60.17283879431961],
                                [24.9320125579834, 60.17283879431961],
                                [24.9320125579834, 60.17221176544357],
                            ]
                        ],
                        "type": "Polygon",
                    },
                    "properties": {"id": "Hankerajaukset_alue_kaavahanke.001"},
                    "type": "Feature",
                }
            ],
        }
