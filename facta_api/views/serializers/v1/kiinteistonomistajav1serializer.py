from rest_framework import serializers
from drf_spectacular.utils import extend_schema_serializer, OpenApiExample
from .kiinteistoaddressv1serializer import KiinteistoAddressV1Serializer


OWNER_TYPES = {
    'H': 'Helsingin Kaupunki',
    'F': 'state owned',
    'P': 'private'
}

@extend_schema_serializer(
    #exclude_fields=('single',),  # schema ignore these fields
    examples=[
    ]
)
class KiinteistonOmistajaV1Serializer(serializers.Serializer):
    kiinteistotunnus = serializers.CharField(max_length=17)
    address = KiinteistoAddressV1Serializer()
    owner_home_municipality = serializers.CharField(max_length=3)

    property_owner_type = serializers.ChoiceField(choices=[(type, desc) for type, desc in OWNER_TYPES.items()])
