# flake8: noqa
from rest_framework import serializers
from drf_spectacular.utils import extend_schema_serializer, OpenApiExample
from .rakennuskieltov1serializer import RakennuskieltoV1Serializer


REKISTERILAJI = {"T": "Tontti", "M": "Maarekisteri"}


@extend_schema_serializer(
    # exclude_fields=('single',),  # schema ignore these fields
    examples=[
        OpenApiExample(
            "Example response",
            summary="Detailed description of fields returned as response",
            description="""
    Fields:
        * kiinteistotunnus: Kiinteistötunnus
        * rekisterilaji: Suunnittelualueella olevan kiinteistön rekisterilaji (M/T)
        * asemakaavan_numero: Voimassa olevan asemakaavan numero
        * asemakaava_voimassa: Milloin kiinteistön asemakaava on tullut voimaan
        * rakennuskiellot: Rakennuskielto/kiellot perusteineen
            """,
            value={
                "kiinteistotunnus": "09143600030009",
                "rekisterilaji": "M",
                "asemakaavan_numero": "12475",
                "asemakaava_voimassa": "2018-04-25",
                "rakennuskiellot": [
                    {
                        "datanomistaja": "Helsinki/KAMI",
                        "antaja_selite": "Lautakunta",
                        "antaja_tunnus": "8",
                        "id": "Rakennuskieltoalue_asemakaavan_laatimiseksi.12",
                        "kunta": "091",
                        "laatu_selite": "§ 58.5 Asemakaavan mukainen toteuttamisen ajoituskielto",
                        "laatu_tunnus": "17540",
                        "luontipvm": "2020-06-10",
                        "muokkauspvm": "2020-06-11",
                        "paatospvm": "2020-06-09",
                        "paattymispvm": "2023-06-29",
                        "paivitetty_tietopalveluun": "2021-05-03",
                        "rakennuskieltotunnus": "12657",
                        "tyyppi": "RK ajoituskielto",
                        "voimaantulopvm": "2020-06-09",
                        "geom": [
                            {
                                "type": "Feature",
                                "geometry": {
                                    "type": "Polygon",
                                    "coordinates": [
                                        [
                                            [60.20347358574124, 24.926132082557697],
                                            [60.20347207422368, 24.926132078434573],
                                            [60.20343224570241, 24.92613741295874],
                                            [60.20339310449809, 24.926153146172446],
                                            [60.20335532032394, 24.926179008840467],
                                            [60.20331953967213, 24.926214558415708],
                                            [60.203286374751784, 24.926259186612043],
                                            [60.20325639301537, 24.926312129814026],
                                            [60.20323010744942, 24.926372482144192],
                                            [60.203207967797795, 24.926439210962325],
                                            [60.203201198243065, 24.926464185078647],
                                            [60.20319035286757, 24.926511174534603],
                                            [60.20317756404759, 24.926587141567452],
                                            [60.203169820152326, 24.926665812273892],
                                            [60.20316725367862, 24.926745840611417],
                                            [60.20316990853806, 24.926825857310806],
                                            [60.203177739306796, 24.92690449330156],
                                            [60.20319061200159, 24.926980403135087],
                                            [60.20320830637297, 24.927052288003182],
                                            [60.203224489049205, 24.927102596064177],
                                            [60.20340239752261, 24.927600711139945],
                                            [60.20385247922556, 24.926951865737937],
                                            [60.203911998262356, 24.926871316871292],
                                            [60.2039519393831, 24.926822790049325],
                                            [60.203973785725815, 24.926797986387285],
                                            [60.204073042361316, 24.92669961714486],
                                            [60.204093958156626, 24.92668169241763],
                                            [60.204176352632786, 24.926619854886187],
                                            [60.204179343792475, 24.926617604579985],
                                            [60.204184617266975, 24.92661236511038],
                                            [60.20418950522922, 24.926605787552628],
                                            [60.20419392404455, 24.926597984450158],
                                            [60.204197798105554, 24.926589089316145],
                                            [60.204201061125836, 24.92657925434894],
                                            [60.204203657274064, 24.926568647828045],
                                            [60.204205214837216, 24.92655989402324],
                                            [60.20420554212918, 24.92655745123403],
                                            [60.20420668344062, 24.926545856144788],
                                            [60.204207061680286, 24.92653406095622],
                                            [60.20420667037627, 24.926522267487808],
                                            [60.20420551622403, 24.926510677530203],
                                            [60.20420361897137, 24.926499489391485],
                                            [60.204201011080954, 24.92648889450429],
                                            [60.204197737174766, 24.926479074150716],
                                            [60.20419724780552, 24.92647803213482],
                                            [60.2041940444973, 24.926470909433355],
                                            [60.20418995710424, 24.926463481881083],
                                            [60.20418949679695, 24.92646291470635],
                                            [60.204184468602925, 24.926456180962088],
                                            [60.204181209959074, 24.926452645958403],
                                            [60.20386106084458, 24.92615155374843],
                                            [60.203854450454216, 24.926145696666957],
                                            [60.20383562650711, 24.92613290613551],
                                            [60.203820445781595, 24.92612647929569],
                                            [60.203816132619735, 24.926125161361696],
                                            [60.2037963023389, 24.9261225948518],
                                            [60.20377796434164, 24.926124879766814],
                                            [60.20374005788018, 24.92613173244237],
                                            [60.20370505417023, 24.926133827139132],
                                            [60.20370201323999, 24.926133826735544],
                                            [60.20349239376431, 24.926132226012275],
                                            [60.20347358574124, 24.926132082557697],
                                        ]
                                    ],
                                },
                                "properties": {
                                    "id": "Rakennuskieltoalue_asemakaavan_laatimiseksi.12"
                                },
                            }
                        ],
                    }
                ],
            },
            request_only=False,  # signal that example only applies to requests
            response_only=True,  # signal that example only applies to responses
        ),
    ]
)
class KiinteistoAllV1Serializer(serializers.Serializer):
    kiinteistotunnus = serializers.CharField(max_length=20)
    rekisterilaji = serializers.ChoiceField(
        choices=[(type, desc) for type, desc in REKISTERILAJI.items()], allow_blank=True
    )
    asemakaavan_numero = serializers.CharField(max_length=20, required=False)
    asemakaava_voimassa = serializers.DateField(format="YYYY-MM-DD", required=False)
    rakennuskiellot = serializers.ListField(
        child=RakennuskieltoV1Serializer(required=False), allow_empty=True
    )
    """
    Suunnittelualueella olevan kiinteistön maanomistajan nimi, osoite
    Onko kiinteistön maanomistajana Helsingin kaupunki/valtio/yksityinen
    Onko kiinteistöllä maanomistajaa, joka on ulkopaikkakuntalainen
    Naapurikiinteistön maanomistajan nimi, osoite
    Suunnittelualueella olevan kiinteistön haltijan nimi, osoite
    Naapurikiinteistön haltijan nimi, osoite
    """
