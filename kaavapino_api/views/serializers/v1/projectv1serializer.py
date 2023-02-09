from rest_framework import serializers
from drf_spectacular.utils import extend_schema_serializer, OpenApiExample


@extend_schema_serializer(
    # exclude_fields=('single',),  # schema ignore these fields
    examples=[
        OpenApiExample(
            "Example response",
            summary="Detailed description of fields returned as response",
            description="""
    Fields:
        * hankenumero: Hankenumero (PW)
        * kaaavnumero: Kaavanumero
        * pinonumero: Pinonumero
        * projektin_nimi: Projektin nimi
        * suunnittelualueen_kuvaus: Suunnittelualueen kuvaus
        * uutta_siirrettavaa_infraa: Onko uutta siirrettävää infraa
        * yksikon_sitova_tavoite: Onko projekti yksikön sitovana tavoitteena
        * diaarinumero: Diaarinumero
        * projektityyppi: Projektityyppi
        * kaavaprosessin_kokoluokka: Kaavaprosessin kokoluokka
        * oasn_paivays: OAS:n päiväys
        * milloin_oas_esillaolo_alkaa: Milloin OAS esilläolo alkaa
        * milloin_oas_esillaolo_paattyy: Milloin OAS esilläolo päättyy
        * milloin_periaatteet_lautakunnassa: Milloin periaatteet lautakunnassa
        * milloin_periaatteet_lautakunnassa_2: Milloin periaatteet lautakunnassa 2
        * milloin_periaatteet_lautakunnassa_3: Milloin periaatteet lautakunnassa 3
        * milloin_periaatteet_lautakunnassa_4: Milloin periaatteet lautakunnassa 4
        * periaatteet_hyvaksytty_kylk: Periaatteet hyväksytty kylk
        * milloin_luonnos_esillaolo_alkaa: Milloin luonnos esilläolo alkaa
        * milloin_luonnos_esillaolo_paattyy: Milloin luonnos esilläolo päättyy
        * milloin_kaavaluonnos_lautakunnassa: Milloin kaavaluonnos lautakunnassa
        * milloin_kaavaluonnos_lautakunnassa_2: Milloin kaavaluonnos lautakunnassa 2
        * milloin_kaavaluonnos_lautakunnassa_3: Milloin kaavaluonnos lautakunnassa 3
        * milloin_kaavaluonnos_lautakunnassa_4: Milloin kaavaluonnos lautakunnassa 4
        * luonnos_hyvaksytty_kylk: Luonnos hyväksytty kylk
        * milloin_kaavaehdotus_lautakunnassa: Milloin kaavaehdotus lautakunnassa
        * milloin_kaavaehdotus_lautakunnassa_2: Milloin kaavaehdotus lautakunnassa 2
        * milloin_kaavaehdotus_lautakunnassa_3: Milloin kaavaehdotus lautakunnassa 3
        * milloin_kaavaehdotus_lautakunnassa_4: Milloin kaavaehdotus lautakunnassa 4
        * ehdotus_hyvaksytty_kylk: Ehdotus hyväksytty kylk
        * milloin_ehdotuksen_nahtavilla_alkaa_iso: Milloin ehdotuksen nähtävilläolo alkaa iso
        * milloin_ehdotuksen_nahtavilla_alkaa_pieni: Milloin ehdotuksen nähtävilläolo alkaa pieni
        * milloin_ehdotuksen_nahtavilla_paattyy: Milloin ehdotuksen nähtävilläolo päättyy
        * milloin_tarkistettu_ehdotus_lautakunnassa: Milloin tarkistettu ehdotus lautakunnassa
        * milloin_tarkistettu_ehdotus_lautakunnassa_2: Milloin tarkistettu ehdotus lautakunnassa 2
        * milloin_tarkistettu_ehdotus_lautakunnassa_3: Milloin tarkistettu ehdotus lautakunnassa 3
        * milloin_tarkistettu_ehdotus_lautakunnassa_4: Milloin tarkistettu ehdotus lautakunnassa 4
        * tarkistettu_ehdotus_hyvaksytty_kylk: Tarkistettu ehdotus hyväksytty kylk
        * muistutusten_lukumaara: Muistutusten lukumäärä
        * hyvaksymispaatos_pvm: Hyväksymispäätös päivämäärä
        * kaavan_hyvaksyjataho: Kaavan hyväksyjätaho
        * voimaantulo_pvm: Voimaantulo päivämäärä
            """,
            value={"pinonumero": "0000027"},
            request_only=False,  # signal that example only applies to requests
            response_only=True,  # signal that example only applies to responses
        ),
    ]
)
class ProjectV1Serializer(serializers.Serializer):
    hankenumero = serializers.CharField(required=False, allow_null=True)
    kaavanumero = serializers.CharField(required=False, allow_null=True)
    pinonumero = serializers.CharField(allow_null=False)
    projektin_nimi = serializers.CharField(allow_null=False)
    suunnittelualueen_kuvaus = serializers.CharField(required=False, allow_null=True)
    uutta_siirrettavaa_infraa = serializers.BooleanField(required=False, allow_null=True)
    yksikon_sitova_tavoite = serializers.BooleanField(required=False, allow_null=True)
    diaarinumero = serializers.CharField(required=False, allow_null=True)
    projektityyppi = serializers.CharField(required=False, allow_null=True)
    kaavaprosessin_kokoluokka = serializers.CharField(required=False, allow_null=True)
    oasn_paivays = serializers.DateField(required=False, allow_null=True)
    milloin_oas_esillaolo_alkaa = serializers.DateField(required=False, allow_null=True)
    milloin_oas_esillaolo_paattyy = serializers.DateField(required=False, allow_null=True)
    milloin_periaatteet_lautakunnassa = serializers.DateField(required=False, allow_null=True)
    milloin_periaatteet_lautakunnassa_2 = serializers.DateField(required=False, allow_null=True)
    milloin_periaatteet_lautakunnassa_3 = serializers.DateField(required=False, allow_null=True)
    milloin_periaatteet_lautakunnassa_4 = serializers.DateField(required=False, allow_null=True)
    periaatteet_hyvaksytty_kylk = serializers.DateField(required=False, allow_null=True)
    milloin_luonnos_esillaolo_alkaa = serializers.DateField(required=False, allow_null=True)
    milloin_luonnos_esillaolo_paattyy = serializers.DateField(required=False, allow_null=True)
    milloin_kaavaluonnos_lautakunnassa = serializers.DateField(required=False, allow_null=True)
    milloin_kaavaluonnos_lautakunnassa_2 = serializers.DateField(required=False, allow_null=True)
    milloin_kaavaluonnos_lautakunnassa_3 = serializers.DateField(required=False, allow_null=True)
    milloin_kaavaluonnos_lautakunnassa_4 = serializers.DateField(required=False, allow_null=True)
    luonnos_hyvaksytty_kylk = serializers.DateField(required=False, allow_null=True)
    milloin_kaavaehdotus_lautakunnassa = serializers.DateField(required=False, allow_null=True)
    milloin_kaavaehdotus_lautakunnassa_2 = serializers.DateField(required=False, allow_null=True)
    milloin_kaavaehdotus_lautakunnassa_3 = serializers.DateField(required=False, allow_null=True)
    milloin_kaavaehdotus_lautakunnassa_4 = serializers.DateField(required=False, allow_null=True)
    ehdotus_hyvaksytty_kylk = serializers.DateField(required=False, allow_null=True)
    milloin_ehdotuksen_nahtavilla_alkaa_iso = serializers.DateField(required=False, allow_null=True)
    milloin_ehdotuksen_nahtavilla_alkaa_pieni = serializers.DateField(required=False, allow_null=True)
    milloin_ehdotuksen_nahtavilla_paattyy = serializers.DateField(required=False, allow_null=True)
    milloin_tarkistettu_ehdotus_lautakunnassa = serializers.DateField(required=False, allow_null=True)
    milloin_tarkistettu_ehdotus_lautakunnassa_2 = serializers.DateField(required=False, allow_null=True)
    milloin_tarkistettu_ehdotus_lautakunnassa_3 = serializers.DateField(required=False, allow_null=True)
    milloin_tarkistettu_ehdotus_lautakunnassa_4 = serializers.DateField(required=False, allow_null=True)
    tarkistettu_ehdotus_hyvaksytty_kylk = serializers.DateField(required=False, allow_null=True)
    muistutusten_lukumaara = serializers.IntegerField(required=False, allow_null=True)
    hyvaksymispaatos_pvm = serializers.DateField(required=False, allow_null=True)
    kaavan_hyvaksyjataho = serializers.CharField(required=False, allow_null=True)
    voimaantulo_pvm = serializers.DateField(required=False, allow_null=True)