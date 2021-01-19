from rest_framework.views import APIView  # pip install django-rest-framework
from django.http import JsonResponse, HttpResponse, HttpResponseBadRequest, \
    HttpResponseNotFound, HttpResponseForbidden, HttpResponseServerError
from drf_spectacular.openapi import AutoSchema
from drf_spectacular.utils import extend_schema, OpenApiParameter
from drf_spectacular.types import OpenApiTypes
import logging
from kaavapino_api.views.serializers.v1 import ChangeV1Serializer

log = logging.getLogger(__name__)


class API(APIView):
    serializer_class = ChangeV1Serializer

    def get(self, request, timestamp=None):
        raise NotImplementedError("Not yet!")

        # Go validate the returned data.
        # It needs to be verifiable by serializer rules. Those are published in Swagger.
        serializer = self.serializer_class(data=kt_data)
        if not serializer.is_valid():
            return HttpResponseServerError("Invalid data received from WFS!")

        return JsonResponse(serializer.validated_data)
