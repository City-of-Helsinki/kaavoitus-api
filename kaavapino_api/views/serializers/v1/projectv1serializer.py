from rest_framework import serializers
from drf_spectacular.utils import extend_schema_serializer, OpenApiExample


@extend_schema_serializer(
    # exclude_fields=('single',),  # schema ignore these fields
    examples=[
        OpenApiExample(
            'Example response',
            summary='Detailed description of fields returned as response',
            description="""
            Example 09100399030101 is
            """,
            value={
                "datanomistaja": "Helsinki/Kami"
            },
            request_only=False,  # signal that example only applies to requests
            response_only=True,  # signal that example only applies to responses
        ),
    ]
)
class ProjectV1Serializer(serializers.Serializer):
    Muistutusten_lkm = serializers.IntegerField(required=False)
    Valitusten_lkm_HAO = serializers.IntegerField(required=False)
    Valitusten_lkm_KHO = serializers.IntegerField(required=False)

    Projektin_nimi = serializers.CharField(max_length=255)
    Diaarinumero = serializers.CharField()
    Hankenumero = serializers.CharField()
    Vastuuhenkilo = serializers.CharField()
    Suunnitteluavustaja = serializers.CharField()
    Kaavan_hyvaksyja = serializers.CharField()
    Kaavanumero = serializers.CharField()
    Kaavan_nimi_FIN = serializers.CharField()
    Kaavan_nimi_SWE = serializers.CharField()
    Ehdotus_hyvaksytty_lautakunnassa = serializers.DateField(required=False)
    Tarkistettu_ehdotus_hyvaksytty_lautakunnassa = serializers.DateField(required=False)
    Kylk_hyvaksynta = serializers.DateField(required=False)
    Ehdotus_toimitettu_kaupunginhallitukselle = serializers.DateField(required=False)
    Valtuusto_hyvaksynyt = serializers.DateField(required=False)
    Kaavaehdotuksen_nahtavillaolo_alkaa = serializers.DateField(required=False)
    Kaavaehdotuksen_nahtavillaolo_paattyy = serializers.DateField(required=False)
    Kaavaehdotus_lautakunnassa = serializers.DateField(required=False)
    Tarkistettu_ehdotus_lautakunnassa = serializers.DateField(required=False)
    Kaava_tullut_voimaan = serializers.DateField(required=False)
    Kaava_tullut_osittain_voimaan = serializers.DateField(required=False)
    Kaava_kumottu = serializers.DateField(required=False)
    Kaava_rauennut = serializers.DateField(required=False)
