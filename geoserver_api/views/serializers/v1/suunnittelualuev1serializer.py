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
                "suunnittelualueen_rajaus": [
                    {
                        "type": "Feature",
                        "geometry": {
                            "type": "Polygon",
                            "coordinates": [
                                [
                                    [60.16268526954202, 24.85560361382704],
                                    [60.16271848524254, 24.85559276360192],
                                    [60.1627510313494, 24.855585846938084],
                                    [60.16279610493577, 24.85558221332046],
                                    [60.162817369359715, 24.85558288866241],
                                    [60.162973458732836, 24.85559341317887],
                                    [60.16303501846143, 24.855699466142454],
                                    [60.16310458039353, 24.856424542341138],
                                    [60.16300968746828, 24.856895227578235],
                                    [60.16271899349028, 24.857007213086252],
                                    [60.16276215597355, 24.857458339972947],
                                    [60.16281205498318, 24.857979979506027],
                                    [60.162828146749966, 24.85814812112544],
                                    [60.16285019101903, 24.858378583474725],
                                    [60.162720843129684, 24.85911986226137],
                                    [60.162707502439375, 24.85919628760949],
                                    [60.163495048679614, 24.858892249027445],
                                    [60.16357586209433, 24.858143245590437],
                                    [60.16361296065637, 24.857714809096887],
                                    [60.163906054283416, 24.855894598863472],
                                    [60.164046446769774, 24.855955812186213],
                                    [60.16418683922309, 24.85601702422923],
                                    [60.16415086280358, 24.855541838401933],
                                    [60.16418082681866, 24.855458176051773],
                                    [60.16443718952046, 24.855367868858668],
                                    [60.16456039048357, 24.855324471054423],
                                    [60.164569421971706, 24.85532166777401],
                                    [60.16459869475206, 24.855317688473885],
                                    [60.16462797593888, 24.85532141040197],
                                    [60.16464361238159, 24.855326605153287],
                                    [60.164656764522434, 24.855332769895224],
                                    [60.16468456792004, 24.855351572608726],
                                    [60.164710910404764, 24.855377496838795],
                                    [60.164720721834975, 24.85538945887011],
                                    [60.16484212811866, 24.855546415960845],
                                    [60.16503482429366, 24.85579555514213],
                                    [60.16504638238458, 24.855811872444345],
                                    [60.165064136728134, 24.855842979582164],
                                    [60.165075360249055, 24.855867425063774],
                                    [60.165079715792295, 24.855878470945736],
                                    [60.16509285301169, 24.855917739266243],
                                    [60.165103323601784, 24.85596011264702],
                                    [60.16510338651943, 24.855960262479257],
                                    [60.16519499543102, 24.855923092037568],
                                    [60.16515360117438, 24.85549571139991],
                                    [60.165141152076956, 24.855368040945194],
                                    [60.16604507390624, 24.85539992976369],
                                    [60.16633085173626, 24.855407469327176],
                                    [60.16664983915069, 24.855416203209426],
                                    [60.16828037163885, 24.855383254710347],
                                    [60.16853167872191, 24.855378072281066],
                                    [60.16956491317837, 24.855357447420484],
                                    [60.170914401083984, 24.844221750367453],
                                    [60.17050530367665, 24.844235668048235],
                                    [60.166019829144865, 24.84439115754545],
                                    [60.165974962523, 24.844393374343525],
                                    [60.16571943454498, 24.84440543423219],
                                    [60.16558427235925, 24.84441246718259],
                                    [60.1654218942266, 24.844348700721454],
                                    [60.165244816094386, 24.844280389994623],
                                    [60.15901586955488, 24.841749486492027],
                                    [60.15809229736619, 24.841374291455246],
                                    [60.15809839324884, 24.85233216234293],
                                    [60.16132980714572, 24.852325461715054],
                                    [60.161500140476235, 24.852712296823213],
                                    [60.16153641280492, 24.853441578223574],
                                    [60.16140763605972, 24.854371090355006],
                                    [60.16148767581398, 24.854583757723073],
                                    [60.16151009489568, 24.854651821061513],
                                    [60.16159809051237, 24.85472728316425],
                                    [60.16158659704654, 24.85508027743823],
                                    [60.16213053248185, 24.85624054958485],
                                    [60.162198983876294, 24.856195068655534],
                                    [60.162617553501654, 24.855946945760863],
                                    [60.16258827830357, 24.855640969805144],
                                    [60.16268526954202, 24.85560361382704],
                                ]
                            ],
                        },
                        "properties": {"id": "Hankerajaukset_alue_kaavahanke.783"},
                    }
                ],
                "suunnittelualueen_pinta_ala": "856041.696977",
                "keskimaarainen_tonttitehokkuus": "0.0",
                "maanalaisten_tilojen_pinta_ala_yht": "0.0",
                "aluevarausten_pinta_alat_yht": "1242503.2089670005",
                "pinta_alan_muutokset_yht": "0.0",
                "suojellut_rakennukset_maara_yht": "0",
                "suojellut_rakennukset_ala_yht": "0.0",
            },
            request_only=False,  # signal that example only applies to requests
            response_only=True,  # signal that example only applies to responses
        ),
    ]
)
class SuunnittelualueV1Serializer(serializers.Serializer):
    suunnittelualueen_rajaus = serializers.JSONField(required=False, allow_null=True)
    suunnittelualueen_pinta_ala = serializers.CharField()
    keskimaarainen_tonttitehokkuus = serializers.CharField(required=False)
    maanalaisten_tilojen_pinta_ala_yht = serializers.CharField(required=False)
    aluevarausten_pinta_alat_yht = serializers.CharField(required=False)
    pinta_alan_muutokset_yht = serializers.CharField(required=False)
    suojellut_rakennukset_maara_yht = serializers.CharField(required=False)
    suojellut_rakennukset_ala_yht = serializers.CharField(required=False)
