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
    RakennuksenOmistajatV1Serializer,
)
from facta_api import hel_facta
from .kiinteisto import KiinteistoAPI
from .rakennus import RakennusAPI
from django.core.cache import cache

log = logging.getLogger(__name__)


class API(KiinteistoAPI, RakennusAPI):
    serializer_class = RakennuksenOmistajatV1Serializer

    def get(self, request, kiinteistotunnus=None):
        if not kiinteistotunnus:
            return HttpResponseBadRequest("Need kiinteistotunnus!")
        ktunnus_to_use = self._format_kiinteistotunnus(kiinteistotunnus)
        if not ktunnus_to_use:
            return HttpResponseBadRequest("Need valid kiinteistotunnus!")
        if not request.auth:
            return HttpResponse(status=401)
        if not request.auth.access_facta:
            return HttpResponseForbidden("No access!")

        cache_key = f'facta_api_rakennuksen_omistajat_get_{kiinteistotunnus}'
        validated_data = cache.get(cache_key)

        if validated_data is None:
            mock_dir = settings.FACTA_DB_MOCK_DATA_DIR
            if mock_dir:
                f_ko = hel_facta.RakennuksenOmistajat(mock_data_dir=mock_dir)
            else:
                f_ko = hel_facta.RakennuksenOmistajat()
            rows = f_ko.get_by_kiinteistotunnus(ktunnus_to_use)
            if not rows:
                return HttpResponseNotFound()

            owner_rows = []
            for row in rows:
                owner = {
                    "kiinteistotunnus": row[1],  # C_KIINTEISTOTUNNUS
                    "address": self._extract_rakennuksen_omistaja_address(row),
                    "y_tunnus": row[14],  # C_LYTUNN
                }
                owner_rows.append(owner)

            ro_data = {"kiinteistotunnus": ktunnus_to_use, "omistajat": owner_rows}

            # Go validate the returned data.
            # It needs to be verifiable by serializer rules. Those are published in Swagger.
            serializer = self.serializer_class(data=ro_data)
            if not serializer.is_valid():
                log.error("Errors: %s" % str(serializer.errors))
                return HttpResponseServerError("Data not formatted correctly!")

            validated_data = serializer.validated_data
            cache.set(cache_key, validated_data, settings.FACTA_CACHE_TIMEOUT)

        return JsonResponse(validated_data)
