from rest_framework import serializers
from drf_spectacular.utils import extend_schema_serializer
from .kiinteistoaddressv1serializer import KiinteistoAddressV1Serializer


@extend_schema_serializer(
    # exclude_fields=('single',),  # schema ignore these fields
    examples=[]
)
class RakennuksenOmistajaV1Serializer(serializers.Serializer):
    kiinteistotunnus = serializers.CharField(max_length=17, required=False)
    address = KiinteistoAddressV1Serializer()
    y_tunnus = serializers.CharField(required=False, allow_null=True, allow_blank=True)
