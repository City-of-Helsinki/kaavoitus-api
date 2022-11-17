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
from ..serializers.v1 import KiinteistonHaltijatV1Serializer
from facta_api import hel_facta
from .kiinteisto import KiinteistoAPI
from django.core.cache import cache

log = logging.getLogger(__name__)


class API(KiinteistoAPI):
    serializer_class = KiinteistonHaltijatV1Serializer

    def get(self, request, kiinteistotunnus=None):
        if not kiinteistotunnus:
            return HttpResponseBadRequest("Need kiinteistotunnus!")
        ktunnus_to_use = self._format_kiinteistotunnus(kiinteistotunnus)
        if not ktunnus_to_use:
            return HttpResponseBadRequest("Need valid kiinteistotunnus!")
        if not request.auth:
            return HttpResponse(status=401)
        facta_creds = request.auth.access_facta
        if not facta_creds:
            return HttpResponseForbidden("No access!")

        cache_key = f'facta_api_kiinteiston_haltijat_get_{kiinteistotunnus}'
        validated_data = cache.get(cache_key)

        if validated_data is None:
            # Confirmed access to Facta Oracle SQL.
            # Mocking?
            mock_dir = settings.FACTA_DB_MOCK_DATA_DIR
            # Go get the data!
            if mock_dir:
                f_kh = hel_facta.KiinteistonHaltijat(mock_data_dir=mock_dir)
            else:
                f_kh = hel_facta.KiinteistonHaltijat(
                    user=facta_creds.username,
                    password=facta_creds.credential,
                    host=facta_creds.host_spec,
                )
            rows = f_kh.get_by_kiinteistotunnus(ktunnus_to_use)
            if not rows:
                return HttpResponseNotFound()

            # Process result:
            occupant_rows = []
            for row in rows:
                if False:
                    for i in range(len(row)):
                        log.debug("%d: %s" % (i, str(row[i])))
                    log.debug("Laji: %s" % row[14])

                occupant = {
                    "kiinteistotunnus": row[2],  # KIINTEISTOTUNNUS
                    "address": self._extract_haltija_address(row),
                    "y_tunnus": row[23],  # C_LYTUNN
                }
                occupant_rows.append(occupant)
            kh_data = {"kiinteistotunnus": ktunnus_to_use, "haltijat": occupant_rows}

            # Go validate the returned data.
            # It needs to be verifiable by serializer rules. Those are published in Swagger.
            serializer = self.serializer_class(data=kh_data)
            if not serializer.is_valid():
                log.error("Errors: %s" % str(serializer.errors))
                return HttpResponseServerError("Data not formatted correctly!")

            validated_data = serializer.validated_data
            cache.set(cache_key, validated_data, settings.FACTA_CACHE_TIMEOUT)

        return JsonResponse(validated_data)
