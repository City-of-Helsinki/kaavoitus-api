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
        * muistutusten_lukumaara: Muistutusten lukumäärä
        * valitusten_lukumaara_HaO: Valitusten lukumäärä HAO
        * valitusten_lukumaara_KHO: Valitusten lukumäärä KHO
        * pinonumero: Pinonumero
        * diaarinumero: Diaarinumero
        * hankenumero: Hankenumero (PW)
        * kaavanlaatija: Vastuuhenkilö
        * kaavan_piirtaja: Suunnitteluavustajan nimi
        * hyvaksyja: Kaavan hyväksyjätaho
        * kaavatunnus: Kaavanumero
        * kaavanimi1: Projektin nimi
        * kaavanimi2: Kaavan (projektin) nimi ruotsiksi
        * kaavan_virallinen_nimi: Kaavan virallinen nimi
        * kaavaehdotus_lautakunnassa: Ehdotus on hyväksytty lautakunnassa
        * tarkistettu_kaavaehdotus_lautakunnassa: Tarkistettu ehdotus on hyväksytty lautakunnassa
        * hyvaksymispvm: Hyväksymispäätöksen päivämäärä
        * tarkistettu_ehdotus_kirje_khs: Milloin ehdotus kirjeellä kaupunginhallitukselle
        * kaavaehdotus_nahtavillealkupvm_iso: Milloin kaavaehdotuksen nähtävilläolo alkaa (L, XL)
        * kaavaehdotus_nahtavillealkupvm_pieni: Milloin kaavaehdotuksen nähtävilläolo alkaa (XS, S, M)
        * kaavaehdotus_nahtavillaviimpvm Milloin kaavaehdotuksen nähtävilläolo päättyy
        * kaavaehdotus_paivatty: Milloin kaavaehdotus on lautakunnassa
        * tarkistettu_kaavaehdotus_paivatty: Milloin tarkistettu ehdotus on lautakunnassa
        * voimaantulopvm: Kaava on tullut voimaan
        * tullut_osittain_voimaan_pvm: Kaava on tullut osittain voimaan
        * kumottu_pvm: Kaava on kumottu
        * rauennut_pvm: Kaava on rauennut
        * kaavan_esittelija_ehdotus: Asemakaavapäällikkönä lautakunnassa, kun ehdotus esitellään
        * kaavan_esittelija_tarkistettu_ehdotus: Asemakaavapäällikkönä lautakunnassa, kun tarkistettu ehdotus esitellään
        * vireilletulopvm: OAS:n päiväys
        * OAS_nahtavillealkupvm: Milloin OAS-aineiston esilläolo alkaa
        * OAS_nahtavillaviimpvm: Milloin OAS-aineiston esilläolo päättyy
        * HaO_paatospvm: Valitusten ratkaisupäivämäärä hallinto-oikeudessa
        * KHO_paatospvm: Valitusten ratkaisupäivämäärä korkeimmassa hallinto-oikeudessa
        * kaavaehdotus_uudelleen_nahtavillealkupvm_iso2: Milloin kaavaehdotuksen nähtävilläolo alkaa (L, XL)
        * kaavaehdotus_uudelleen_nahtavillealkupvm_pieni2: Milloin kaavaehdotuksen nähtävilläolo alkaa (XS, S, M)
        * kaavaehdotus_uudelleen_nahtavillaviimpvm_2: Milloin kaavaehdotuksen nähtävilläolo päättyy
        * kaavaehdotus_uudelleen_nahtavillealkupvm_iso3: Milloin kaavaehdotuksen nähtävilläolo alkaa (L, XL)
        * kaavaehdotus_uudelleen_nahtavillealkupvm_pieni3: Milloin kaavaehdotuksen nähtävilläolo alkaa (XS, S, M)
        * kaavaehdotus_uudelleen_nahtavillaviimpvm_3: Milloin kaavaehdotuksen nähtävilläolo päättyy
        * kaavaehdotus_uudelleen_nahtavillealkupvm_iso4: Milloin kaavaehdotuksen nähtävilläolo alkaa (L, XL)
        * kaavaehdotus_uudelleen_nahtavillealkupvm_pieni4: Milloin kaavaehdotuksen nähtävilläolo alkaa (XS, S, M)
        * kaavaehdotus_uudelleen_nahtavillaviimpvm_4: Milloin kaavaehdotuksen nähtävilläolo päättyy
            """,
            value={"pinonumero": "0000027"},
            request_only=False,  # signal that example only applies to requests
            response_only=True,  # signal that example only applies to responses
        ),
    ]
)
class ProjectV1Serializer(serializers.Serializer):
    muistutusten_lukumaara = serializers.IntegerField(required=False)
    valitusten_lukumaara_HaO = serializers.IntegerField(required=False)
    valitusten_lukumaara_KHO = serializers.IntegerField(required=False)
    pinonumero = serializers.CharField()
    diaarinumero = serializers.CharField()
    hankenumero = serializers.CharField()
    kaavanlaatija = serializers.CharField()
    kaavan_piirtaja = serializers.CharField()
    hyvaksyja = serializers.CharField()
    kaavatunnus = serializers.CharField()
    kaavanimi1 = serializers.CharField()
    kaavanimi2 = serializers.CharField()
    kaavan_virallinen_nimi = serializers.CharField()
    kaavaehdotus_lautakunnassa = serializers.DateField(required=False)
    tarkistettu_kaavaehdotus_lautakunnassa = serializers.DateField(required=False)
    hyvaksymispvm = serializers.DateField(required=False)
    tarkistettu_ehdotus_kirje_khs = serializers.DateField(required=False)
    kaavaehdotus_nahtavillealkupvm_iso = serializers.DateField(required=False)
    kaavaehdotus_nahtavillealkupvm_pieni = serializers.DateField(required=False)
    kaavaehdotus_nahtavillaviimpvm = serializers.DateField(required=False)
    kaavaehdotus_paivatty = serializers.DateField(required=False)
    tarkistettu_kaavaehdotus_paivatty = serializers.DateField(required=False)
    voimaantulopvm = serializers.DateField(required=False)
    tullut_osittain_voimaan_pvm = serializers.DateField(required=False)
    kumottu_pvm = serializers.DateField(required=False)
    rauennut_pvm = serializers.DateField(required=False)
    kaavan_esittelija_ehdotus = serializers.CharField(required=False)
    kaavan_esittelija_tarkistettu_ehdotus = serializers.CharField(required=False)
    vireilletulopvm = serializers.DateField(required=False)
    OAS_nahtavillealkupvm = serializers.DateField(required=False)
    OAS_nahtavillaviimpvm = serializers.DateField(required=False)
    HaO_paatospvm = serializers.DateField(required=False)
    KHO_paatospvm = serializers.DateField(required=False)
    kaavaehdotus_uudelleen_nahtavillealkupvm_iso2 = serializers.DateField(
        required=False
    )
    kaavaehdotus_uudelleen_nahtavillealkupvm_pieni2 = serializers.DateField(
        required=False
    )
    kaavaehdotus_uudelleen_nahtavillaviimpvm_2 = serializers.DateField(required=False)
    kaavaehdotus_uudelleen_nahtavillealkupvm_iso3 = serializers.DateField(
        required=False
    )
    kaavaehdotus_uudelleen_nahtavillealkupvm_pieni3 = serializers.DateField(
        required=False
    )
    kaavaehdotus_uudelleen_nahtavillaviimpvm_3 = serializers.DateField(required=False)
    kaavaehdotus_uudelleen_nahtavillealkupvm_iso4 = serializers.DateField(
        required=False
    )
    kaavaehdotus_uudelleen_nahtavillealkupvm_pieni4 = serializers.DateField(
        required=False
    )
    kaavaehdotus_uudelleen_nahtavillaviimpvm_4 = serializers.DateField(required=False)
    # TBD later
    # HL51_muutettu_huomautukset = serializers.CharField(required=False)
    # HL51_muutettu_poydalle_ehdotus = serializers.CharField(required=False)
    # H51_muutettu_poydalle_tarkistettu_ehdotus = serializers.CharField(required=False)
    # HL51_muutettu_aska = serializers.CharField(required=False)
    # HL51_muutettu_khs = serializers.CharField(required=False)
