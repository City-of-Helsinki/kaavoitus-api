from rest_framework import serializers
from drf_spectacular.utils import extend_schema_serializer, OpenApiExample


@extend_schema_serializer(
    # exclude_fields=('single',),  # schema ignore these fields
    examples=[
        OpenApiExample(
            "Example response",
            summary="Detailed description of fields returned as response",
            description="""
            Example 09100399030101 is part of Espa, esplanade and urban park in downtown Helsinki.
            Group 9903 indicates a public space, a park.

            Fields:
            * datanomistaja: Owner of this data in City of Helsinki
            * id: Database unique id
            * gml_id: Database unique id in GML (ISO 19136:2007)
            * kiinteistotunnus: zero padded 14 digit (3-3-4-4) representation of field 'kiinteisto'
            * kiinteisto: dash-separated value of kunta-sijaintialue-ryhma-yksikko
            * kunta: Number from list https://tilastokeskus.fi/fi/luokitukset/kunta/
            * sijaintialue: region
            * ryhma: group in region or if public space, following type codes are used:
              * 9901 Streets
              * 9902 Marketplaces and squares
              * 9903 Parks
              * 9904 Sports
              * 9905 Recreational areas
              * 9906 Traffic
              * 9907 Danger
              * 9908 Special and preserved areas
              * 9909 Water
            * yksikko: unit in group
            * luontipvm: Database data creation date
            * muokkauspvm": Database data modification date
            * paivitetty_tietopalveluun": Database read date
            * "rekisterointipvm": Data creation date (earliest 1st Jan 1800)
            * geom: String, GML representation of the geographical area for this data
            """,
            value={
                "datanomistaja": "Helsinki/Kami",
                "id": "Kiinteisto_alue.29976",
                "kiinteisto": "91-3-9903-101",
                "kiinteistotunnus": "09100399030101",
                "kunta": "091",
                "luontipvm": "2013-12-09",
                "muokkauspvm": "2014-06-10",
                "paivitetty_tietopalveluun": "2021-05-11",
                "rekisterointipvm": "1980-05-30",
                "ryhma": "9903",
                "sijaintialue": "003",
                "yksikko": "0101",
                "geom": [
                    {
                        "type": "Feature",
                        "geometry": {
                            "type": "MultiPolygon",
                            "coordinates": [
                                [
                                    [
                                        [60.16770787604104, 24.945822596882344],
                                        [60.167190728234246, 24.945878041085354],
                                        [60.16728067217075, 24.949376521148313],
                                        [60.167792992022136, 24.949324179702018],
                                        [60.16770787604104, 24.945822596882344],
                                    ]
                                ]
                            ],
                        },
                        "properties": {"id": "Kiinteisto_alue.29976"},
                    }
                ],
            },
            request_only=False,  # signal that example only applies to requests
            response_only=True,  # signal that example only applies to responses
        ),
    ]
)
class KiinteistoV1Serializer(serializers.Serializer):
    datanomistaja = serializers.CharField(max_length=40)
    id = serializers.CharField()
    kiinteisto = serializers.CharField(max_length=24)
    kiinteistotunnus = serializers.CharField(max_length=20)
    kunta = serializers.CharField(min_length=3, max_length=3)
    luontipvm = serializers.DateField(format="YYYY-MM-DD")
    muokkauspvm = serializers.DateField(format="YYYY-MM-DD")
    paivitetty_tietopalveluun = serializers.DateField(format="YYYY-MM-DD")
    rekisterointipvm = serializers.DateField(format="YYYY-MM-DD")
    ryhma = serializers.CharField(min_length=4, max_length=4)
    sijaintialue = serializers.CharField(min_length=3, max_length=3)
    yksikko = serializers.CharField(min_length=4, max_length=4)
    gml_id = serializers.CharField(max_length=80, required=False)
    geom = serializers.JSONField(required=False, allow_null=True)
