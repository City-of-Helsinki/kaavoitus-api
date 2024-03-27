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
            * kaavatunnus: Kaavatunnus
            * date: Päivämäärä
            * date_type: Päivämäärän tyyppi (lainvoimaisuuspvm / vahvistamispvm)
            """,
            value={},
            request_only=False,  # signal that example only applies to requests
            response_only=True,  # signal that example only applies to responses
        ),
    ]
)
class KaavaV1Serializer(serializers.Serializer):
    kaavatunnus = serializers.CharField(allow_null=False, allow_blank=False)
    date = serializers.DateField(allow_null=False, format="%d.%m.%Y", input_formats=["%Y-%m-%d"])
    date_type = serializers.CharField(allow_null=False, allow_blank=False)


@extend_schema_serializer(
    examples=[
        OpenApiExample(
            "Example response",
            summary="Detailed description of fields returned as response",
            description="""
            Example:
            Fields:
            * hankenumero: Hankenumero
            * kaavat: Lista kaavoista
            """,
            value={},
            request_only=False,  # signal that example only applies to requests
            response_only=True,  # signal that example only applies to responses
        ),
    ]
)
class KaavatV1Serializer(serializers.Serializer):
    hankenumero = serializers.CharField(allow_null=False, allow_blank=False)
    kaavat = KaavaV1Serializer(many=True)
