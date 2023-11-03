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
            * voimassa_asemakaavat: Voimassaolevat asemakaavat
            * voimassa_olevat_rakennuskiellot: Voimassaolevat rakennuskiellot
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
    voimassa_asemakaavat = serializers.CharField(allow_blank=True)
    voimassa_olevat_rakennuskiellot = serializers.CharField(allow_blank=True)

    maanomistus_kaupunki = serializers.CharField(max_length=6)
    maanomistus_valtio = serializers.CharField(max_length=6)
    maanomistus_yksityinen = serializers.CharField(max_length=6)
    maanomistaja_ulkopaikkakunta = serializers.CharField(max_length=6)
    haltija_ulkopaikkakunta = serializers.CharField(max_length=6)
