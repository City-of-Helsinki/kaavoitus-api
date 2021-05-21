from facta_api.views.serializers.v1.rakennuksenomistajatv1serializer import (
    RakennuksenOmistajatV1Serializer,
)
from rest_framework import serializers
from .kiinteistonomistajav1serializer import KiinteistonOmistajaV1Serializer
from .kiinteistonhaltijav1serializer import KiinteistonHaltijaV1Serializer


class NaapuritV1Serializer(serializers.Serializer):
    kiinteistotunnus = serializers.CharField(max_length=17)
    omistajat = KiinteistonOmistajaV1Serializer(many=True)
    haltijat = KiinteistonHaltijaV1Serializer(many=True)
    rakennuksen_omistajat = RakennuksenOmistajatV1Serializer(many=True)
