from rest_framework import serializers
from .kiinteistonhaltijav1serializer import KiinteistonHaltijaV1Serializer


class KiinteistonHaltijatV1Serializer(serializers.Serializer):
    kiinteistotunnus = serializers.CharField(max_length=17)
    haltijat = KiinteistonHaltijaV1Serializer(many=True)
