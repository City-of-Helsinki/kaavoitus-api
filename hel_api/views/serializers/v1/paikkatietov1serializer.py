from rest_framework import serializers
from drf_spectacular.utils import extend_schema_serializer, OpenApiExample

from .rakennuskieltov1serializer import RakennuskieltoV1Serializer
from .asemakaavav1serializer import AsemakaavaV1Serializer


@extend_schema_serializer(
    examples=[
        OpenApiExample(
            "Example response",
            summary="Detailed description of fields returned as response",
            description="""
            Example:
            Fields:
            * voimassa_asemakaavat_fieldset: Voimassaolevat asemakaavat
            * voimassa_olevat_rakennuskiellot_fieldset: Voimassaolevat rakennuskiellot
            * maanomistus_kaupunki: Onko alueella kaupungin maanomistusta
            * maanomistus_valtio: Onko alueella valtion maanomistusta
            * maanomistus_yksityinen: Onko alueella yksityisen maanomistusta
            * maanomistaja_ulkopaikkakunta: Onko alueella ulkopaikkakuntalaisen maanomistusta
            * haltija_ulkopaikkakunta: Onko alueella ulkopaikkakuntalaisia haltijoita
            """,
            value={},
            request_only=False,  # signal that example only applies to requests
            response_only=True,  # signal that example only applies to responses
        ),
    ]
)
class PaikkatietoV1Serializer(serializers.Serializer):
    voimassa_asemakaavat_fieldset = AsemakaavaV1Serializer(many=True)
    voimassa_olevat_rakennuskiellot_fieldset = RakennuskieltoV1Serializer(many=True)

    maanomistus_kaupunki = serializers.CharField(max_length=6)
    maanomistus_valtio = serializers.CharField(max_length=6)
    maanomistus_yksityinen = serializers.CharField(max_length=6)
    maanomistaja_ulkopaikkakunta = serializers.CharField(max_length=6)
    haltija_ulkopaikkakunta = serializers.CharField(max_length=6)
