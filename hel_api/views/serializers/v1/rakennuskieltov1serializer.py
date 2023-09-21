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
            * rakennuskiellon_numero: Rakennuskiellon numero
            * rakennuskiellon_peruste: Rakennuskiellon peruste
            """,
            value={},
            request_only=False,  # signal that example only applies to requests
            response_only=True,  # signal that example only applies to responses
        ),
    ]
)
class RakennuskieltoV1Serializer(serializers.Serializer):
    rakennuskiellon_numero = serializers.CharField()
    rakennuskiellon_peruste = serializers.CharField()
