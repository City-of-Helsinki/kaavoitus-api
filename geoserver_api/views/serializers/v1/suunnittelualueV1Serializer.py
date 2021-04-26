from rest_framework import serializers
from drf_spectacular.utils import extend_schema_serializer, OpenApiExample


@extend_schema_serializer(
    #exclude_fields=('single',),  # schema ignore these fields
    examples=[
        OpenApiExample(
            'Example response',
            summary='Detailed description of fields returned as response',
            description="""
            Example
            """,
            value={
                "suunnittelualueen_rajaus": "<gml:Polygon></gml:Polygon>",
                "suunnittelualueen_pinta_ala": "856041.696977",
                "keskimaarainen_tonttitehokkuus": "0.0",
                "maanalaisten_tilojen_pinta_ala_yht": "0.0",
                "aluevarausten_pinte_alat_yht": "335802.8163190007",
                # "pinta_alan_muutokset_yht": "0.0"
                "suojellut_rakennukset_maara_yht": "0",
                "suojellut_rakennukset_ala_yht": "0.0"
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
    #pinta_alan_muutokset_yht = serializers.CharField(required=False)
    suojellut_rakennukset_maara_yht = serializers.CharField(required=False)
    suojellut_rakennukset_ala_yht = serializers.CharField(required=False)
