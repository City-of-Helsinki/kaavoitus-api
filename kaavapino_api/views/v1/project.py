from django.http.response import (
    HttpResponseForbidden,
    HttpResponseNotFound,
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
        attribute_data = project_data.get("attribute_data", {})
        if not attribute_data:
            return HttpResponseNotFound()

        data = {
            "muistutusten_lkm": attribute_data.get("muistutusten_lukumaara"),
            "valitusten_lkm_HaO": attribute_data.get(
                "valitusten_lukumaara_hallinto_oikeus"
            ),
            "valitusten_lkm_KHO": attribute_data.get("valitusten_lukumaara_kho"),
            "pinonumero": project_data.get("pino_number"),
            "diaarinumero": attribute_data.get("diaarinumero"),
            "hankenumero": attribute_data.get("hankenumero"),
            "kaavanlaatija": attribute_data.get("vastuuhenkilo_nimi"),
            "kaavan_mallintaja": attribute_data.get("suunnitteluavustaja_nimi"),
            "hyvaksyja": attribute_data.get("kaavan_hyvaksyjataho"),
            "kaavatunnus": attribute_data.get("kaavanumero"),
            "kaavanimi1": attribute_data.get("projektin_nimi"),
            "kaavanimi2": attribute_data.get("kaavan_nimi_ruotsiksi"),
            "kaavan_virallinen_nimi": attribute_data.get("kaavan_nimi"),
            "kaavaehdotus_lautakunnassa": attribute_data.get("ehdotus_hyvaksytty_kylk"),
            "tarkistettu_kaavaehdotus_lautakunnassa": attribute_data.get(
                "tarkistettu_ehdotus_hyvaksytty_kylk"
            ),
            "hyvaksymispvm": attribute_data.get("hyvaksymispaatos_pvm"),
            "tarkistettu_ehdotus_kirje_khs": attribute_data.get(
                "toteutunut_kirje_kaupunginhallitukselle"
            ),
            "kaavaehdotus_nahtaville_alkupvm_iso": attribute_data.get(
                "milloin_ehdotuksen_nahtavilla_alkaa_iso"
            ),
            "kaavaehdotus_nahtaville_alkupvm_pieni": attribute_data.get(
                "milloin_ehdotuksen_nahtavilla_alkaa_pieni"
            ),
            "kaavaehdotus_nahtavilla_viimpvm": attribute_data.get(
                "milloin_ehdotuksen_nahtavilla_paattyy"
            ),
            "kaavaehdotus_paivatty": attribute_data.get(
                "milloin_kaavaehdotus_lautakunnassa"
            ),
            "tarkistettu_kaavaehdotus_paivatty": attribute_data.get(
                "milloin_tarkistettu_ehdotus_lautakunnassa"
            ),
            "voimaantulopvm": attribute_data.get("voimaantulo_pvm"),
            "tullut_osittain_voimaan_pvm": attribute_data.get(
                "tullut_osittain_voimaan_pvm"
            ),
            "kumottu_pvm": attribute_data.get("kumottu_pvm"),
            "rauennut_pvm": attribute_data.get("rauennut"),
            "kaavan_esittelija_ehdotus": attribute_data.get("akp_kylk_ehdotus"),
            "kaavan_esittelija_tarkistettu_ehdotus": attribute_data.get(
                "akp_kylk_tarkistettu_ehdotus"
            ),
            "vireilletulopvm": attribute_data.get("oasn_paivays"),
            "OAS_nahtavillealkupvm": attribute_data.get("milloin_oas_esillaolo_alkaa"),
            "OAS_nahtavillaviimpvm": attribute_data.get(
                "milloin_oas_esillaolo_paattyy"
            ),
            "HaO_paatospvm": attribute_data.get("valitusten_ratkaisu_hallinto_oikeus"),
            "KHO_paatospvm": attribute_data.get("valitusten_ratkaisu_kho"),
            "kaavaehdotus_uudelleen_nahtaville_alkupvm_iso2": attribute_data.get(
                "milloin_ehdotuksen_nahtavilla_alkaa_iso_2"
            ),
            "kaavaehdotus_uudelleen_nahtaville_alkupvm_pieni2": attribute_data.get(
                "milloin_ehdotuksen_nahtavilla_alkaa_pieni_2"
            ),
            "kaavaehdotus_uudelleen_nahtavilla_viimpvm_2": attribute_data.get(
                "milloin_ehdotuksen_nahtavilla_paattyy_2"
            ),
            "kaavaehdotus_uudelleen_nahtaville_alkupvm_iso3": attribute_data.get(
                "milloin_ehdotuksen_nahtavilla_alkaa_iso_3"
            ),
            "kaavaehdotus_uudelleen_nahtaville_alkupvm_pieni3": attribute_data.get(
                "milloin_ehdotuksen_nahtavilla_alkaa_pieni_3"
            ),
            "kaavaehdotus_uudelleen_nahtavilla_viimpvm_3": attribute_data.get(
                "milloin_ehdotuksen_nahtavilla_paattyy_3"
            ),
            "kaavaehdotus_uudelleen_nahtaville_alkupvm_iso4": attribute_data.get(
                "milloin_ehdotuksen_nahtavilla_alkaa_iso_4"
            ),
            "kaavaehdotus_uudelleen_nahtaville_alkupvm_pieni4": attribute_data.get(
                "milloin_ehdotuksen_nahtavilla_alkaa_pieni_4"
            ),
            "kaavaehdotus_uudelleen_nahtavilla_viimpvm_4": attribute_data.get(
                "milloin_ehdotuksen_nahtavilla_paattyy_4"
            ),
        }

        # Go validate the returned data.
        # It needs to be verifiable by serializer rules. Those are published in Swagger.
        serializer = self.serializer_class(data=data)
        if not serializer.is_valid():
            return HttpResponseServerError("Invalid data received from Kaavapino")

        return JsonResponse(serializer.validated_data)
