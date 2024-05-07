from rest_framework import serializers
from drf_spectacular.utils import extend_schema_serializer, OpenApiExample


@extend_schema_serializer(
    examples=[
        OpenApiExample(
            "Example response",
            summary="Detailed description of fields returned as response",
            description="""
            Example:
            Fields:
            * rakennuskieltotunnus: Rakennuskieltotunnus
            * date: Päivämäärä
            * date_type: Päivämäärän tyyppi
            * selite: Selite
            """,
            value={},
            request_only=False,  # signal that example only applies to requests
            response_only=True,  # signal that example only applies to responses
        ),
    ]
)
class RakennuskieltoV1Serializer(serializers.Serializer):
    rakennuskieltotunnus = serializers.CharField(allow_blank=False, allow_null=False)
    date = serializers.DateField(allow_null=False, format="%d.%m.%Y", input_formats=["%Y-%m-%d"])
    date_type = serializers.CharField(allow_null=False, allow_blank=False)
    selite = serializers.CharField(allow_null=False, allow_blank=False)


@extend_schema_serializer(
    examples=[
        OpenApiExample(
            "Example response",
            summary="Detailed description of fields returned as response",
            description="""
            Example:
            Fields:
            * hankenumero: Hankenumero
            * rakennuskiellot: Voimassaolevat rakennuskiellot
            """,
            value={},
            request_only=False,  # signal that example only applies to requests
            response_only=True,  # signal that example only applies to responses
        ),
    ]
)
class RakennuskiellotV1Serializer(serializers.Serializer):
    hankenumero = serializers.CharField(allow_null=False, allow_blank=False)
    rakennuskiellot = RakennuskieltoV1Serializer(many=True)
