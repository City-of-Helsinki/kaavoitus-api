from rest_framework.views import APIView  # pip install django-rest-framework
from django.http import (
    JsonResponse,
    HttpResponse,
    HttpResponseBadRequest,
    HttpResponseNotFound,
    HttpResponseForbidden,
    HttpResponseServerError,
)
from drf_spectacular.utils import extend_schema
from drf_spectacular.types import OpenApiTypes
import logging
from geoserver_api.hki_geoserver.kiinteistotunnus import Kiinteistotunnus
from geoserver_api.views.serializers.v1 import KiinteistoV1Serializer

log = logging.getLogger(__name__)


class API(APIView):
    serializer_class = KiinteistoV1Serializer

    def get(self, request, kiinteistotunnus=None):
        if not kiinteistotunnus:
            return HttpResponseBadRequest("Need kiinteistotunnus!")

        if not request.auth:
            return HttpResponse(status=401)
        geoserver_creds = request.auth.access_geoserver
        if not geoserver_creds:
            return HttpResponseForbidden("No access!")

        # Confirmed access to GeoServer.
        # Go get the data!
        kt = Kiinteistotunnus(
            username=geoserver_creds.username, password=geoserver_creds.credential
        )
        kt_data = kt.get(kiinteistotunnus)
        if not kt_data:
            log.error("%s not found!" % kiinteistotunnus)
            return HttpResponseNotFound()

        log.info("Kiinteistötunnus: %s" % (kt_data["kiinteisto"]))
        kt_data["geom"] = kt.get_geometry(kt_data)

        # Go validate the returned data.
        # It needs to be verifiable by serializer rules. Those are published in Swagger.
        serializer = self.serializer_class(data=kt_data)
        if not serializer.is_valid():
            return HttpResponseServerError("Invalid data received from WFS!")

        return JsonResponse(serializer.validated_data)

    @extend_schema(responses={200: OpenApiTypes.OBJECT})
    def post(self, request):
        pass
