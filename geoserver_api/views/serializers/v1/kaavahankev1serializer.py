# flake8: noqa
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
        * tietopalvelu_id:
        * hankenumero:
        * kaavahankkeen_nimi:
        * kaavahankkeen_kuvaus:
        * vastuuhenkilo:
        * vastuuyksikko:
        * muut_vastuuhenkilot:
        * toimintasuunnitelmaan:
        * diaarinumero:
        * kaavanumero:
        * hanketyyppi:
        * kaavaprosessi:
        * maankayttosopimus:
        * kaavavaihe:
        * oas_pvm:
        * asuminen_yhteensa_k_m2:
        * toimitila_yhteensa_k_m2:
        * suunnitteluperiaatteet_suunniteltu_pvm:
        * suunnitteluperiaatteet_hyvaksytty_pvm:
        * luonnos_suunniteltu_pvm:
        * luonnos_hyvaksytty_pvm:
        * ehdotus_suunniteltu_pvm:
        * ehdotus_hyvaksytty_pvm:
        * tarkistettu_ehdotus_suunniteltu_pvm:
        * tarkistettu_ehdotus_hyvaksytty_pvm:
        * hyvaksytty_pvm:
        * hyvaksyja:
        * tavoite_1:
        * tavoite_2:
        * tavoite_3:
        * aineistot_pwssa:
        * luontipvm:
        * muokkauspvm:
        * selostus:
        * datanomistaja:
        * paivitetty_tietopalveluun:
        * id:
        * srs:
        * geom: String, GML representation of the geographical area for this data
            """,
            value={
                "tietopalvelu_id": 1053,
                "hankenumero": "0592_13",
                "kaavahankkeen_nimi": "Merikorttikuja 6, asemakaavan muutos",
                "kaavahankkeen_kuvaus": "Olemassa olevan kerrostalotontin täydennysrakentaminen.",
                "vastuuhenkilo": "UKKONEN JUSSI VILI MIKAEL",
                "vastuuyksikko": "VUOSAARI-VARTIOKYLÄ",
                "muut_vastuuhenkilot": "LIKE/Janne Antila, TEK/Leivo Pekka",
                "toimintasuunnitelmaan": "Ei",
                "diaarinumero": "HEL 2017-010023",
                "kaavanumero": "12553",
                "hanketyyppi": "asemakaava",
                "kaavaprosessi": "M",
                "maankayttosopimus": "kyllä",
                "kaavavaihe": "07 Hyväksytty",
                "oas_pvm": "04.04.2018",
                "asuminen_yhteensa_k_m2": 9900,
                "toimitila_yhteensa_k_m2": 200,
                "suunnitteluperiaatteet_suunniteltu_pvm": "null",
                "suunnitteluperiaatteet_hyvaksytty_pvm": "null",
                "luonnos_suunniteltu_pvm": "null",
                "luonnos_hyvaksytty_pvm": "null",
                "ehdotus_suunniteltu_pvm": "null",
                "ehdotus_hyvaksytty_pvm": "null",
                "tarkistettu_ehdotus_suunniteltu_pvm": "16.04.2019",
                "tarkistettu_ehdotus_hyvaksytty_pvm": "null",
                "hyvaksytty_pvm": "31.03.2021",
                "hyvaksyja": "Kvsto",
                "tavoite_1": "1.1 Asuntotuotannon edistäminen",
                "tavoite_2": "1.5 Elävät, omaleimaiset ja turvalliset kaupunginosat",
                "tavoite_3": "2.2 Kumppanuus ja osallisuus toimintatapana vahvistuvat",
                "aineistot_pwssa": "pw://hels000601.helsinki1.hki.local:HKIPW/Documents/P{ad07509c-e419-4bda-b5a7-7fe71e5baacb}/",
                "luontipvm": "2018-02-07",
                "muokkauspvm": "2018-02-07",
                "selostus": "null",
                "datanomistaja": "Helsinki/MAKA",
                "paivitetty_tietopalveluun": "2021-05-12",
                "id": "Hankerajaukset_alue_kaavahanke.1053",
                "srs": "urn:ogc:def:crs:EPSG::3879",
                "geom": [
                    {
                        "type": "Feature",
                        "geometry": {
                            "type": "Polygon",
                            "coordinates": [
                                [
                                    [60.21628762979331, 25.129485638715988],
                                    [60.21533520601964, 25.12935510847131],
                                    [60.21525123891026, 25.13182959391695],
                                    [60.21503046984468, 25.131928552015655],
                                    [60.215192278800046, 25.133223155604057],
                                    [60.21524695428115, 25.133660629712733],
                                    [60.21660588988698, 25.133011195177044],
                                    [60.21655477098117, 25.132306703814645],
                                    [60.21642015079162, 25.13229605757576],
                                    [60.21645579707743, 25.130475506603347],
                                    [60.21627398719765, 25.130231702047492],
                                    [60.21628762979331, 25.129485638715988],
                                ]
                            ],
                        },
                        "properties": {"id": "Hankerajaukset_alue_kaavahanke.1053"},
                    }
                ],
            },
            request_only=False,  # signal that example only applies to requests
            response_only=True,  # signal that example only applies to responses
        ),
    ]
)
class KaavahankeV1Serializer(serializers.Serializer):
    tietopalvelu_id = serializers.CharField()
    hankenumero = serializers.CharField()
    kaavahankkeen_nimi = serializers.CharField()
    kaavahankkeen_kuvaus = serializers.CharField()
    vastuuhenkilo = serializers.CharField()
    vastuuyksikko = serializers.CharField()
    muut_vastuuhenkilot = serializers.CharField()
    toimintasuunnitelmaan = serializers.CharField()
    diaarinumero = serializers.CharField()
    kaavanumero = serializers.CharField()
    hanketyyppi = serializers.CharField()
    kaavaprosessi = serializers.CharField()
    maankayttosopimus = serializers.CharField()
    kaavavaihe = serializers.CharField()
    oas_pvm = serializers.DateField(format="DD.MM.YYYY", allow_null=True)
    asuminen_yhteensa_k_m2 = serializers.CharField()
    toimitila_yhteensa_k_m2 = serializers.CharField()
    suunnitteluperiaatteet_suunniteltu_pvm = serializers.DateField(
        format="YYYY-MM-DD", allow_null=True
    )
    suunnitteluperiaatteet_hyvaksytty_pvm = serializers.DateField(
        format="YYYY-MM-DD", allow_null=True
    )
    luonnos_suunniteltu_pvm = serializers.DateField(
        format="YYYY-MM-DD", allow_null=True
    )
    luonnos_hyvaksytty_pvm = serializers.DateField(format="YYYY-MM-DD", allow_null=True)
    ehdotus_suunniteltu_pvm = serializers.DateField(
        format="YYYY-MM-DD", allow_null=True
    )
    ehdotus_hyvaksytty_pvm = serializers.DateField(format="YYYY-MM-DD", allow_null=True)
    tarkistettu_ehdotus_suunniteltu_pvm = serializers.DateField(
        format="DD.MM.YYYY", allow_null=True
    )
    tarkistettu_ehdotus_hyvaksytty_pvm = serializers.DateField(
        format="YYYY-MM-DD", allow_null=True
    )
    hyvaksytty_pvm = serializers.DateField(format="DD.MM.YYYY", allow_null=True)
    hyvaksyja = serializers.CharField()
    tavoite_1 = serializers.CharField()
    tavoite_2 = serializers.CharField()
    tavoite_3 = serializers.CharField()
    aineistot_pwssa = serializers.CharField()
    luontipvm = serializers.DateField(format="YYYY-MM-DD", allow_null=True)
    muokkauspvm = serializers.DateField(format="YYYY-MM-DD", allow_null=True)
    selostus = serializers.CharField()
    datanomistaja = serializers.CharField()
    paivitetty_tietopalveluun = serializers.DateField(
        format="YYYY-MM-DD", allow_null=True
    )
    id = serializers.CharField()
    srs = serializers.CharField()
    geom = serializers.JSONField(required=False, allow_null=True)
