from django.http.response import (
    HttpResponseForbidden,
    HttpResponseServerError,
    JsonResponse,
)
from rest_framework.views import APIView  # pip install django-rest-framework
from django.http import (
    HttpResponse,
    HttpResponseBadRequest,
)
import logging
from kaavapino_api.views.serializers.v1 import ProjectV1Serializer
from kaavapino_api.kaavapino.kaavapino_client import KaavapinoClient

log = logging.getLogger(__name__)


class API(APIView):
    serializer_class = ProjectV1Serializer

    def get(self, request, pinonro=None):
        if not pinonro:
            return HttpResponseBadRequest("Need pinonro!")

        if not request.auth:
            return HttpResponse(status=401)

        kaavapino_creds = request.auth.access_kaavapino
        if not kaavapino_creds:
            return HttpResponseForbidden("No access!")

        self.client = KaavapinoClient(api_key=kaavapino_creds.credential)

        # Fetch project data from kaavopino
        project_data = self.client.get_projects(pinonro)
        # log.info(project_data)

        data = {
            "muistutusten_lukumaara": project_data.get("attribute_data").get(
                "muistutusten_lukumaara"
            ),
            "valitusten_lukumaara_HaO": project_data.get("attribute_data").get(
                "valitusten_lukumaara_hallinto_oikeus"
            ),
            "valitusten_lukumaara_KHO": project_data.get("attribute_data").get(
                "valitusten_lukumaara_kho"
            ),
            "pinonumero": project_data.get("pino_number"),
            "diaarinumero": project_data.get("attribute_data").get("diaarinumero"),
            "hankenumero": project_data.get("attribute_data").get("hankenumero"),
            "kaavanlaatija": project_data.get("attribute_data").get(
                "vastuuhenkilo_nimi"
            ),
            "kaavan_piirtaja": project_data.get("attribute_data").get(
                "suunnitteluavustaja_nimi"
            ),
            "hyvaksyja": project_data.get("attribute_data").get("kaavan_hyvaksyjataho"),
            "kaavatunnus": project_data.get("attribute_data").get("kaavanumero"),
            "kaavanimi1": project_data.get("attribute_data").get("projektin_nimi"),
            "kaavanimi2": project_data.get("attribute_data").get(
                "kaavan_nimi_ruotsiksi"
            ),
            "kaavan_virallinen_nimi": project_data.get("attribute_data").get(
                "kaavan_nimi"
            ),
            "kaavaehdotus_lautakunnassa": project_data.get("attribute_data").get(
                "ehdotus_hyvaksytty_kylk"
            ),
            "tarkistettu_kaavaehdotus_lautakunnassa": project_data.get(
                "attribute_data"
            ).get("tarkistettu_ehdotus_hyvaksytty_kylk"),
            "hyvaksymispvm": project_data.get("attribute_data").get(
                "hyvaksymispaatos_pvm"
            ),
            "tarkistettu_ehdotus_kirje_khs": project_data.get("attribute_data").get(
                "toteutunut_kirje_kaupunginhallitukselle"
            ),
            "kaavaehdotus_nahtavillealkupvm_iso": project_data.get(
                "attribute_data"
            ).get("milloin_ehdotuksen_nahtavilla_alkaa_iso"),
            "kaavaehdotus_nahtavillealkupvm_pieni": project_data.get(
                "attribute_data"
            ).get("milloin_ehdotuksen_nahtavilla_alkaa_pieni"),
            "kaavaehdotus_nahtavillaviimpvm": project_data.get("attribute_data").get(
                "milloin_ehdotuksen_nahtavilla_paattyy"
            ),
            "kaavaehdotus_paivatty": project_data.get("attribute_data").get(
                "milloin_kaavaehdotus_lautakunnassa"
            ),
            "tarkistettu_kaavaehdotus_paivatty": project_data.get("attribute_data").get(
                "milloin_tarkistettu_ehdotus_lautakunnassa"
            ),
            "voimaantulopvm": project_data.get("attribute_data").get("voimaantulo_pvm"),
            "tullut_osittain_voimaan_pvm": project_data.get("attribute_data").get(
                "tullut_osittain_voimaan_pvm"
            ),
            "kumottu_pvm": project_data.get("attribute_data").get("kumottu_pvm"),
            "rauennut_pvm": project_data.get("attribute_data").get("rauennut"),
            "kaavan_esittelija_ehdotus": project_data.get("attribute_data").get(
                "akp_kylk_ehdotus"
            ),
            "kaavan_esittelija_tarkistettu_ehdotus": project_data.get(
                "attribute_data"
            ).get("akp_kylk_tarkistettu_ehdotus"),
            "vireilletulopvm": project_data.get("attribute_data").get("oasn_paivays"),
            "OAS_nahtavillealkupvm": project_data.get("attribute_data").get(
                "milloin_oas_esillaolo_alkaa"
            ),
            "OAS_nahtavillaviimpvm": project_data.get("attribute_data").get(
                "milloin_oas_esillaolo_paattyy"
            ),
            "HaO_paatospvm": project_data.get("attribute_data").get(
                "valitusten_ratkaisu_hallinto_oikeus"
            ),
            "KHO_paatospvm": project_data.get("attribute_data").get(
                "valitusten_ratkaisu_kho"
            ),
            "kaavaehdotus_uudelleen_nahtavillealkupvm_iso2": project_data.get(
                "attribute_data"
            ).get("milloin_ehdotuksen_nahtavilla_alkaa_iso_2"),
            "kaavaehdotus_uudelleen_nahtavillealkupvm_pieni2": project_data.get(
                "attribute_data"
            ).get("milloin_ehdotuksen_nahtavilla_alkaa_pieni_2"),
            "kaavaehdotus_uudelleen_nahtavillaviimpvm_2": project_data.get(
                "attribute_data"
            ).get("milloin_ehdotuksen_nahtavilla_paattyy_2"),
            "kaavaehdotus_uudelleen_nahtavillealkupvm_iso3": project_data.get(
                "attribute_data"
            ).get("milloin_ehdotuksen_nahtavilla_alkaa_iso_3"),
            "kaavaehdotus_uudelleen_nahtavillealkupvm_pieni3": project_data.get(
                "attribute_data"
            ).get("milloin_ehdotuksen_nahtavilla_alkaa_pieni_3"),
            "kaavaehdotus_uudelleen_nahtavillaviimpvm_3": project_data.get(
                "attribute_data"
            ).get("milloin_ehdotuksen_nahtavilla_paattyy_3"),
            "kaavaehdotus_uudelleen_nahtavillealkupvm_iso4": project_data.get(
                "attribute_data"
            ).get("milloin_ehdotuksen_nahtavilla_alkaa_iso_4"),
            "kaavaehdotus_uudelleen_nahtavillealkupvm_pieni4": project_data.get(
                "attribute_data"
            ).get("milloin_ehdotuksen_nahtavilla_alkaa_pieni_4"),
            "kaavaehdotus_uudelleen_nahtavillaviimpvm_4": project_data.get(
                "attribute_data"
            ).get("milloin_ehdotuksen_nahtavilla_paattyy_4"),
        }

        # Go validate the returned data.
        # It needs to be verifiable by serializer rules. Those are published in Swagger.
        serializer = self.serializer_class(data=data)
        if not serializer.is_valid():
            return HttpResponseServerError("Invalid data received from Kaavapino")

        return JsonResponse(serializer.validated_data)
