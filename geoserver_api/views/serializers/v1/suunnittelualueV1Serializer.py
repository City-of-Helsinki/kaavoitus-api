# flake8: noqa
from rest_framework import serializers
from drf_spectacular.utils import extend_schema_serializer, OpenApiExample


@extend_schema_serializer(
    # exclude_fields=('single',),  # schema ignore these fields
    examples=[
        OpenApiExample(
            "Example response",
            summary="Detailed description of fields returned as response",
            description="""
    Fields:
        * suunnittelualueen_rajaus: Suunnittelualueen rajaus (GeoJSON)
        * suunnittelualueen_pinta_ala: Suunnittelualueen pinta-ala              
        * keskimaarainen_tonttitehokkuus: Tonttien keskimääräinen tehokkuusluku                   
        * maanalaisten_tilojen_pinta_ala_yht: Maanalaisten tilojen pinta-ala yhteensä
        * aluevarausten_pinta_alat_yht: Aluevarausten pinta-alat yhteensä  
        * pinta_alan_muutokset_yht: Pinta-alan muutokset yhteensä
        * suojellut_rakennukset_maara_yht: Suojellut rakennukset, lukumäärä
        * suojellut_rakennukset_ala_yht: Suojellut rakennukset, kerrosala yhteensä
            """,
            value={
                "suunnittelualueen_rajaus": '[{"type": "Feature", "geometry": "{ \\"type\\": \\"Polygon\\", \\"coordinates\\": [ [ [ 60.162685269542017, 24.855603613827039 ], [ 60.162718485242543, 24.855592763601919 ], [ 60.162751031349401, 24.855585846938084 ], [ 60.162796104935772, 24.85558221332046 ], [ 60.162817369359715, 24.855582888662411 ], [ 60.162973458732836, 24.85559341317887 ], [ 60.163035018461429, 24.855699466142454 ], [ 60.163104580393529, 24.856424542341138 ], [ 60.163009687468282, 24.856895227578235 ], [ 60.16271899349028, 24.857007213086252 ], [ 60.162762155973553, 24.857458339972947 ], [ 60.162812054983178, 24.857979979506027 ], [ 60.162828146749966, 24.858148121125438 ], [ 60.162850191019032, 24.858378583474725 ], [ 60.162720843129684, 24.85911986226137 ], [ 60.162707502439375, 24.859196287609489 ], [ 60.163495048679614, 24.858892249027445 ], [ 60.163575862094334, 24.858143245590437 ], [ 60.163612960656373, 24.857714809096887 ], [ 60.163906054283416, 24.855894598863472 ], [ 60.164046446769774, 24.855955812186213 ], [ 60.164186839223092, 24.856017024229232 ], [ 60.164150862803581, 24.855541838401933 ], [ 60.164180826818658, 24.855458176051773 ], [ 60.164437189520463, 24.855367868858668 ], [ 60.164560390483572, 24.855324471054423 ], [ 60.164569421971706, 24.85532166777401 ], [ 60.164598694752058, 24.855317688473885 ], [ 60.164627975938878, 24.85532141040197 ], [ 60.164643612381589, 24.855326605153287 ], [ 60.164656764522434, 24.855332769895224 ], [ 60.164684567920041, 24.855351572608726 ], [ 60.164710910404764, 24.855377496838795 ], [ 60.164720721834975, 24.855389458870111 ], [ 60.164842128118657, 24.855546415960845 ], [ 60.165034824293663, 24.85579555514213 ], [ 60.165046382384581, 24.855811872444345 ], [ 60.165064136728134, 24.855842979582164 ], [ 60.165075360249055, 24.855867425063774 ], [ 60.165079715792295, 24.855878470945736 ], [ 60.165092853011693, 24.855917739266243 ], [ 60.165103323601784, 24.855960112647018 ], [ 60.165103386519426, 24.855960262479257 ], [ 60.165194995431023, 24.855923092037568 ], [ 60.165153601174381, 24.855495711399911 ], [ 60.165141152076956, 24.855368040945194 ], [ 60.16604507390624, 24.855399929763689 ], [ 60.166330851736262, 24.855407469327176 ], [ 60.166649839150693, 24.855416203209426 ], [ 60.168280371638851, 24.855383254710347 ], [ 60.168531678721912, 24.855378072281066 ], [ 60.16956491317837, 24.855357447420484 ], [ 60.170914401083984, 24.844221750367453 ], [ 60.170505303676649, 24.844235668048235 ], [ 60.166019829144865, 24.844391157545449 ], [ 60.165974962523002, 24.844393374343525 ], [ 60.165719434544982, 24.84440543423219 ], [ 60.165584272359247, 24.84441246718259 ], [ 60.165421894226597, 24.844348700721454 ], [ 60.165244816094386, 24.844280389994623 ], [ 60.159015869554878, 24.841749486492027 ], [ 60.158092297366188, 24.841374291455246 ], [ 60.158098393248842, 24.852332162342929 ], [ 60.161329807145719, 24.852325461715054 ], [ 60.161500140476235, 24.852712296823213 ], [ 60.161536412804921, 24.853441578223574 ], [ 60.161407636059721, 24.854371090355006 ], [ 60.16148767581398, 24.854583757723073 ], [ 60.161510094895682, 24.854651821061513 ], [ 60.161598090512371, 24.854727283164252 ], [ 60.161586597046544, 24.85508027743823 ], [ 60.162130532481847, 24.85624054958485 ], [ 60.162198983876294, 24.856195068655534 ], [ 60.162617553501654, 24.855946945760863 ], [ 60.162588278303573, 24.855640969805144 ], [ 60.162685269542017, 24.855603613827039 ] ] ] }", "properties": {"id": "asemakaava.30"}}]',
                "suunnittelualueen_pinta_ala": "856041.696977",
                "keskimaarainen_tonttitehokkuus": "0.0",
                "maanalaisten_tilojen_pinta_ala_yht": "0.0",
                "aluevarausten_pinte_alat_yht": "335802.8163190007",
                # "pinta_alan_muutokset_yht": "0.0"
                "suojellut_rakennukset_maara_yht": "0",
                "suojellut_rakennukset_ala_yht": "0.0",
            },
            request_only=False,  # signal that example only applies to requests
            response_only=True,  # signal that example only applies to responses
        ),
    ]
)
class SuunnittelualueV1Serializer(serializers.Serializer):
    suunnittelualueen_rajaus = serializers.CharField()
    suunnittelualueen_pinta_ala = serializers.CharField()
    keskimaarainen_tonttitehokkuus = serializers.CharField(required=False)
    maanalaisten_tilojen_pinta_ala_yht = serializers.CharField(required=False)
    aluevarausten_pinta_alat_yht = serializers.CharField(required=False)
    # pinta_alan_muutokset_yht = serializers.CharField(required=False)
    suojellut_rakennukset_maara_yht = serializers.CharField(required=False)
    suojellut_rakennukset_ala_yht = serializers.CharField(required=False)
