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
            * hankenumero: Hankenumero
            * kiinteistotunnukset: Kiinteistotunnukset hankenumerolle
            """,
            value={},
            request_only=False,  # signal that example only applies to requests
            response_only=True,  # signal that example only applies to responses
        ),
    ]
)
class KiinteistotunnusV1Serializer(serializers.Serializer):
    hankenumero = serializers.CharField(allow_blank=False, allow_null=False)
    kiinteistotunnukset = serializers.ListField(
        child=serializers.CharField(allow_blank=False, allow_null=False)
    )
