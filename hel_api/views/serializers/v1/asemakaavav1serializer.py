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
            * voimassa_asemakaava_numero: Asemakaavan numero
            * milloin_asemakaava_tullut_voimaan: Milloin asemakaava on tullut voimaan
            """,
            value={},
            request_only=False,  # signal that example only applies to requests
            response_only=True,  # signal that example only applies to responses
        ),
    ]
)
class AsemakaavaV1Serializer(serializers.Serializer):
    voimassa_asemakaava_numero = serializers.CharField(max_length=24)
    milloin_asemakaava_tullut_voimaan = serializers.DateField(format="YYYY-MM-DD")
