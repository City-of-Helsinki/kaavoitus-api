from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from drf_spectacular.utils import extend_schema
from drf_spectacular.types import OpenApiTypes

import logging

from common_auth.models import ExtAuthCred

logger = logging.getLogger(__name__)


class Ping(APIView):
    permission_classes = []  # Enable ping request without authentication

    @extend_schema(
        responses={200: OpenApiTypes.STR}
    )
    def get(self, request, *args, **kwargs):
        return Response("pong")


class Status(APIView):
    permission_classes = []  # Enable status request without authentication

    @extend_schema(
        responses={
            200: OpenApiTypes.STR,
            503: OpenApiTypes.STR
        }
    )
    def get(self, request, *args, **kwargs):
        try:
            ExtAuthCred.objects.count()
            return Response("Kaavoitus-api ok")
        except Exception as exc:
            logger.error("Exception in Status request", exc)
            return Response("Kaavoitus-api not ok", status=status.HTTP_503_SERVICE_UNAVAILABLE)
