from rest_framework import serializers
from drf_spectacular.utils import extend_schema_serializer, OpenApiExample
from .rakennuskieltov1serializer import RakennuskieltoV1Serializer


REKISTERILAJI = {
    'T': 'Tontti',
    'M': "Maarekisteri"
}

@extend_schema_serializer(
    #exclude_fields=('single',),  # schema ignore these fields
    examples=[
        OpenApiExample(
            'Example response',
            summary='Detailed description of fields returned as response',
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
                    "geom": "[{\"type\": \"Feature\", \"geometry\": \"{ \\\"type\\\": \\\"Polygon\\\", \\\"coordinates\\\": [ [ [ 60.203473585741243, 24.926132082557697 ], [ 60.203472074223683, 24.926132078434573 ], [ 60.203432245702409, 24.926137412958742 ], [ 60.20339310449809, 24.926153146172446 ], [ 60.203355320323944, 24.926179008840467 ], [ 60.20331953967213, 24.926214558415708 ], [ 60.203286374751784, 24.926259186612043 ], [ 60.203256393015373, 24.926312129814026 ], [ 60.203230107449421, 24.926372482144192 ], [ 60.203207967797795, 24.926439210962325 ], [ 60.203201198243065, 24.926464185078647 ], [ 60.203190352867573, 24.926511174534603 ], [ 60.203177564047593, 24.926587141567452 ], [ 60.203169820152326, 24.926665812273892 ], [ 60.203167253678622, 24.926745840611417 ], [ 60.203169908538058, 24.926825857310806 ], [ 60.203177739306796, 24.92690449330156 ], [ 60.203190612001592, 24.926980403135087 ], [ 60.203208306372971, 24.927052288003182 ], [ 60.203224489049205, 24.927102596064177 ], [ 60.203402397522609, 24.927600711139945 ], [ 60.20385247922556, 24.926951865737937 ], [ 60.203911998262356, 24.926871316871292 ], [ 60.203951939383103, 24.926822790049325 ], [ 60.203973785725815, 24.926797986387285 ], [ 60.204073042361316, 24.926699617144859 ], [ 60.204093958156626, 24.926681692417631 ], [ 60.204176352632786, 24.926619854886187 ], [ 60.204179343792475, 24.926617604579985 ], [ 60.204184617266975, 24.92661236511038 ], [ 60.204189505229223, 24.926605787552628 ], [ 60.204193924044553, 24.926597984450158 ], [ 60.204197798105554, 24.926589089316145 ], [ 60.204201061125836, 24.92657925434894 ], [ 60.204203657274064, 24.926568647828045 ], [ 60.204205214837216, 24.926559894023239 ], [ 60.204205542129181, 24.926557451234029 ], [ 60.204206683440617, 24.926545856144788 ], [ 60.204207061680286, 24.926534060956222 ], [ 60.204206670376273, 24.926522267487808 ], [ 60.204205516224029, 24.926510677530203 ], [ 60.20420361897137, 24.926499489391485 ], [ 60.204201011080954, 24.926488894504288 ], [ 60.204197737174766, 24.926479074150716 ], [ 60.204197247805517, 24.92647803213482 ], [ 60.204194044497299, 24.926470909433355 ], [ 60.204189957104241, 24.926463481881083 ], [ 60.20418949679695, 24.926462914706349 ], [ 60.204184468602925, 24.926456180962088 ], [ 60.204181209959074, 24.926452645958403 ], [ 60.203861060844581, 24.926151553748429 ], [ 60.203854450454216, 24.926145696666957 ], [ 60.203835626507107, 24.926132906135511 ], [ 60.203820445781595, 24.926126479295689 ], [ 60.203816132619735, 24.926125161361696 ], [ 60.203796302338901, 24.926122594851801 ], [ 60.20377796434164, 24.926124879766814 ], [ 60.203740057880182, 24.926131732442371 ], [ 60.203705054170229, 24.926133827139132 ], [ 60.20370201323999, 24.926133826735544 ], [ 60.203492393764307, 24.926132226012275 ], [ 60.203473585741243, 24.926132082557697 ] ] ] }\", \"properties\": {\"id\": \"Rakennuskieltoalue_asemakaavan_laatimiseksi.12\"}}]"
                    }
                ]
            },
            request_only=False,  # signal that example only applies to requests
            response_only=True,  # signal that example only applies to responses
        ),
    ]
)
class KiinteistoAllV1Serializer(serializers.Serializer):

    kiinteistotunnus = serializers.CharField(max_length=20)
    rekisterilaji = serializers.ChoiceField(choices=[(type, desc) for type, desc in REKISTERILAJI.items()], allow_null=True)
    asemakaavan_numero = serializers.CharField(max_length=20, required=False)
    asemakaava_voimassa = serializers.DateField(format='YYYY-MM-DD', required=False)
    rakennuskiellot = serializers.ListField(child=RakennuskieltoV1Serializer(required=False), allow_empty=True)
    """
    Suunnittelualueella olevan kiinteistön maanomistajan nimi, osoite
    Onko kiinteistön maanomistajana Helsingin kaupunki/valtio/yksityinen
    Onko kiinteistöllä maanomistajaa, joka on ulkopaikkakuntalainen
    Naapurikiinteistön maanomistajan nimi, osoite
    Suunnittelualueella olevan kiinteistön haltijan nimi, osoite
    Naapurikiinteistön haltijan nimi, osoite
    """
