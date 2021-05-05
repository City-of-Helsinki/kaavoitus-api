from rest_framework import serializers
from .kiinteistonomistajav1serializer import KiinteistonOmistajaV1Serializer
from .kiinteistonhaltijav1serializer import KiinteistonHaltijaV1Serializer
from .naapuritV1serializer import NaapuritV1Serializer


class KiinteistonDataV1Serializer(serializers.Serializer):
    kiinteistotunnus = serializers.CharField(max_length=17)
    omistajat = KiinteistonOmistajaV1Serializer(many=True)
    haltijat = KiinteistonHaltijaV1Serializer(many=True)
    naapurit = serializers.ListField(
        child=NaapuritV1Serializer(required=False), allow_empty=True
    )
