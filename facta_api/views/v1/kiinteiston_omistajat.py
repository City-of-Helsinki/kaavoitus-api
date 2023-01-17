from django.http import (
    JsonResponse,
    HttpResponse,
    HttpResponseBadRequest,
    HttpResponseNotFound,
    HttpResponseForbidden,
    HttpResponseServerError,
)
import logging
from django.conf import settings
from ..serializers.v1 import (
    KiinteistonOmistajatV1Serializer,
)
from facta_api import hel_facta
from .kiinteisto import KiinteistoAPI
from django.core.cache import cache
from api_project.utils import format_kiinteistotunnus

log = logging.getLogger(__name__)


class API(KiinteistoAPI):
    serializer_class = KiinteistonOmistajatV1Serializer

    def get(self, request, kiinteistotunnus=None):
        if not kiinteistotunnus:
            return HttpResponseBadRequest("Need kiinteistotunnus!")
        ktunnus_to_use = format_kiinteistotunnus(kiinteistotunnus)
        if not ktunnus_to_use:
            return HttpResponseBadRequest("Need valid kiinteistotunnus!")
        if not request.auth:
            return HttpResponse(status=401)
        if not request.auth.access_facta:
            return HttpResponseForbidden("No access!")

        cache_key = f'facta_api_kiinteiston_omistajat_get_{kiinteistotunnus}'
        validated_data = cache.get(cache_key)

        if validated_data is None:
            # Confirmed access to Facta Oracle SQL.
            # Mocking?
            mock_dir = settings.FACTA_DB_MOCK_DATA_DIR
            # Go get the data!
            if mock_dir:
                f_ko = hel_facta.KiinteistonOmistajat(mock_data_dir=mock_dir)
            else:
                f_ko = hel_facta.KiinteistonOmistajat()
            rows = f_ko.get_by_kiinteistotunnus(ktunnus_to_use)
            if not rows:
                return HttpResponseNotFound()

            # Process result:
            owner_rows = []
            for row in rows:
                if False:
                    for i in range(len(row)):
                        log.debug("%d: %s" % (i, str(row[i])))
                    log.debug("Laji: %s" % row[14])

                # KiinteistonOmistajaV1Serializer.OWNER_TYPES
                if row[14] == "10":  # C_LAJI
                    # Helsinki
                    owner_type = "H"
                elif row[14] in ["8", "11"]:  # C_LAJI
                    # Govt. of Finland
                    owner_type = "F"
                else:
                    # Private
                    owner_type = "P"

                owner = {
                    "kiinteistotunnus": row[2],  # KIINTEISTOTUNNUS
                    "address": self._extract_omistaja_address(row),
                    "owner_home_municipality": row[17],  # C_KOTIKUNT
                    "property_owner_type": owner_type,
                    "y_tunnus": row[16],  # C_LYTUNN
                }
                if owner not in owner_rows:
                    owner_rows.append(owner)
            ko_data = {"kiinteistotunnus": ktunnus_to_use, "omistajat": owner_rows}

            # Go validate the returned data.
            # It needs to be verifiable by serializer rules. Those are published in Swagger.
            serializer = self.serializer_class(data=ko_data)
            if not serializer.is_valid():
                log.error("Errors: %s" % str(serializer.errors))
                return HttpResponseServerError("Data not formatted correctly!")

            validated_data = serializer.validated_data
            cache.set(cache_key, validated_data, settings.FACTA_CACHE_TIMEOUT)

        return JsonResponse(validated_data)
