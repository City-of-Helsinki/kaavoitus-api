from rest_framework import serializers
from .rakennuksenomistajav1serializer import RakennuksenOmistajaV1Serializer


class RakennuksenOmistajatV1Serializer(serializers.Serializer):
    kiinteistotunnus = serializers.CharField(max_length=17)
    omistajat = RakennuksenOmistajaV1Serializer(many=True,required=False)
