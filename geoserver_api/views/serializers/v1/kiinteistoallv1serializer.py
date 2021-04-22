from rest_framework import serializers
from drf_spectacular.utils import extend_schema_serializer, OpenApiExample
from .rakennuskieltov1serializer import RakennuskieltoV1Serializer


REKISTERILAJI = {
    'T': 'Tontti',
    'M': "Maarekisteri"
}

@extend_schema_serializer(
    #exclude_fields=('single',),  # schema ignore these fields
    examples=[
        OpenApiExample(
            'Example response',
            summary='Detailed description of fields returned as response',
            description="""
            Example
            """,
            value={
                "datanomistaja": "Helsinki/Kami",
                "id": 156,
            },
            request_only=False,  # signal that example only applies to requests
            response_only=True,  # signal that example only applies to responses
        ),
    ]
)
class KiinteistoAllV1Serializer(serializers.Serializer):

    kiinteistotunnus = serializers.CharField(max_length=20)
    rekisterilaji = serializers.ChoiceField(choices=[(type, desc) for type, desc in REKISTERILAJI.items()], allow_null=True)
    asemakaavan_numero = serializers.CharField(max_length=20, required=False)
    asemakaava_voimassa = serializers.DateField(format='YYYY-MM-DD', required=False)
    rakennuskiellot = serializers.ListField(child=RakennuskieltoV1Serializer(required=False), allow_empty=True)
    """
    Suunnittelualueella olevan kiinteistön maanomistajan nimi, osoite
    Onko kiinteistön maanomistajana Helsingin kaupunki/valtio/yksityinen
    Onko kiinteistöllä maanomistajaa, joka on ulkopaikkakuntalainen
    Naapurikiinteistön maanomistajan nimi, osoite
    Suunnittelualueella olevan kiinteistön haltijan nimi, osoite
    Naapurikiinteistön haltijan nimi, osoite
    """
