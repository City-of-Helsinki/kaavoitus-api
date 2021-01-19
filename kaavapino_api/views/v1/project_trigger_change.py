from rest_framework.views import APIView  # pip install django-rest-framework
from django.http import JsonResponse, HttpResponse, HttpResponseBadRequest, \
    HttpResponseNotFound, HttpResponseForbidden, HttpResponseServerError
from drf_spectacular.openapi import AutoSchema
from drf_spectacular.utils import extend_schema, OpenApiParameter
from drf_spectacular.types import OpenApiTypes
import logging

log = logging.getLogger(__name__)


class API(APIView):

    def patch(self, request, pinonro=None):
        if not pinonro:
            return HttpResponseBadRequest("Need pinonro!")

        raise NotImplementedError("Not yet!")

        # Go validate the returned data.
        # It needs to be verifiable by serializer rules. Those are published in Swagger.
        serializer = self.serializer_class(data=kt_data)
        if not serializer.is_valid():
            return HttpResponseServerError("Invalid data received from WFS!")

        return JsonResponse(serializer.validated_data)
