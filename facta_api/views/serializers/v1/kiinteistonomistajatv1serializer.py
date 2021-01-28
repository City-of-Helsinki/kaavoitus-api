from rest_framework import serializers
from drf_spectacular.utils import extend_schema_serializer, OpenApiExample
from .kiinteistonomistajav1serializer import KiinteistonOmistajaV1Serializer


class KiinteistonOmistajatV1Serializer(serializers.Serializer):
    kiinteistotunnus = serializers.CharField(max_length=17)
    omistajat = KiinteistonOmistajaV1Serializer(many=True)
