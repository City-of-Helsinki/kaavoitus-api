from rest_framework.views import APIView  # pip install django-rest-framework
from django.http import JsonResponse, HttpResponse, HttpResponseBadRequest, \
    HttpResponseNotFound, HttpResponseForbidden, HttpResponseServerError
from drf_spectacular.openapi import AutoSchema
from drf_spectacular.utils import extend_schema, OpenApiParameter
from drf_spectacular.types import OpenApiTypes
import logging
import lxml.etree as etree
from ..serializers.v1 import KiinteistonHaltijatV1Serializer
from facta_api import hel_facta
from .kiinteisto import KiinteistoAPI

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

        # Confirmed access to Facta Oracle SQL.
        # Go get the data!
        f_kh = hel_facta.KiinteistonHaltijat(facta_creds.username,
                                              facta_creds.credential,
                                              facta_creds.host_spec)
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
                'kiinteistotunnus': row[2], # KIINTEISTOTUNNUS
                'address': self._extract_haltija_address(row),
            }
            occupant_rows.append(occupant)
        kh_data = {
            'kiinteistotunnus': ktunnus_to_use,
            'haltijat': occupant_rows
        }

        # Go validate the returned data.
        # It needs to be verifiable by serializer rules. Those are published in Swagger.
        serializer = self.serializer_class(data=kh_data)
        if not serializer.is_valid():
            log.error("Errors: %s" % str(serializer.errors))

            return HttpResponseServerError("Data not formatted correctly!")

        return JsonResponse(serializer.validated_data)
