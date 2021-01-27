from rest_framework import serializers
from drf_spectacular.utils import extend_schema_serializer, OpenApiExample


@extend_schema_serializer(
    examples=[
        OpenApiExample(
            'Example response',
            summary='Detailed description of fields returned as response',
            description="""
            Example:
            Fields:
            * Tyyppi: "RK asemakaavan laatimiseksi" tai "RK yleiskaavan laatimiseksi"
            """,
            value={

            },
            request_only=False,  # signal that example only applies to requests
            response_only=True,  # signal that example only applies to responses
        ),
    ]
)
class RakennuskieltoV1Serializer(serializers.Serializer):
    datanomistaja = serializers.CharField(max_length=40)
    antaja_selite = serializers.CharField()
    antaja_tunnus = serializers.CharField()
    id = serializers.CharField()
    kunta = serializers.CharField(min_length=3, max_length=3)
    laatu_selite = serializers.CharField()
    laatu_tunnus = serializers.CharField()
    luontipvm = serializers.DateField(format='YYYY-MM-DD')
    muokkauspvm = serializers.DateField(format='YYYY-MM-DD')
    paatospvm = serializers.DateField(format='YYYY-MM-DD')
    paattymispvm = serializers.DateField(format='YYYY-MM-DD')
    paivitetty_tietopalveluun = serializers.DateField(format='YYYY-MM-DD')
    rakennuskieltotunnus = serializers.CharField()
    tyyppi = serializers.CharField()
    voimaantulopvm = serializers.DateField(format='YYYY-MM-DD')
    gml_id = serializers.CharField(max_length=80, required=False)
    geom = serializers.CharField(required=False)
