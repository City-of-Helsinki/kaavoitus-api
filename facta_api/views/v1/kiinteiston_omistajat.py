from rest_framework.views import APIView  # pip install django-rest-framework
from django.http import JsonResponse, HttpResponse, HttpResponseBadRequest, \
    HttpResponseNotFound, HttpResponseForbidden, HttpResponseServerError
from drf_spectacular.openapi import AutoSchema
from drf_spectacular.utils import extend_schema, OpenApiParameter
from drf_spectacular.types import OpenApiTypes
import logging
import lxml.etree as etree
from ..serializers.v1 import KiinteistonOmistajatV1Serializer
from facta_api import hel_facta

log = logging.getLogger(__name__)


class API(APIView):
    serializer_class = KiinteistonOmistajatV1Serializer

    @staticmethod
    def _format_kiinteistotunnus(kiinteistotunnus):
        if len(kiinteistotunnus) == 17 and kiinteistotunnus.count('-') == 3:
            # Looking good
            return kiinteistotunnus

        if len(kiinteistotunnus) == 14 and kiinteistotunnus.count('-') == 0:
            kt_out = '%s-%s-%s-%s' % (
                kiinteistotunnus[:3],
                kiinteistotunnus[3:6],
                kiinteistotunnus[6:10],
                kiinteistotunnus[10:],
            )
            log.debug("Formatted kiinteistötunnus '%s' into valid format." % kiinteistotunnus)

            return kt_out

        # Fail, the input isn't valid
        return None

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
        f_ko = hel_facta.KiinteistonOmistajat(facta_creds.username,
                                              facta_creds.credential,
                                              facta_creds.host_spec)
        row = f_ko.get_by_kiinteistotunnus(ktunnus_to_use)
        if not row:
            return HttpResponseNotFound()

        # Process result:
        for i in range(len(row)):
            log.debug("%d: %s" % (i, str(row[i])))

        ko_data = {}

        # Go validate the returned data.
        # It needs to be verifiable by serializer rules. Those are published in Swagger.
        serializer = self.serializer_class(data=ko_data)
        if not serializer.is_valid():
            return HttpResponseServerError("Invalid data received from WFS!")

        return JsonResponse(serializer.validated_data)
