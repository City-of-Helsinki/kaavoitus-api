from rest_framework import serializers
from drf_spectacular.utils import extend_schema_serializer, OpenApiExample


@extend_schema_serializer(
    #exclude_fields=('single',),  # schema ignore these fields
    examples=[
    ]
)
class KiinteistoAddressV1Serializer(serializers.Serializer):
    first_names = serializers.CharField(max_length=110, allow_null=True)
    last_name = serializers.CharField(max_length=100)
    address = serializers.CharField(max_length=271)
    address2 = serializers.CharField(max_length=100, allow_null=True)
    zip_code = serializers.CharField(max_length=5)
    city_fin = serializers.CharField(max_length=402)
    city_swe = serializers.CharField(max_length=402)
