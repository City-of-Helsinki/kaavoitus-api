from rest_framework.views import APIView  # pip install django-rest-framework
from rest_framework import permissions
from django.http import HttpResponseBadRequest
from drf_spectacular.openapi import AutoSchema
from drf_spectacular.utils import extend_schema, OpenApiParameter
from drf_spectacular.types import OpenApiTypes
from common_auth.authentication import TokenAuthentication
from .v1.neighbourhood import API as APIv1


class API(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]
    schema = AutoSchema()
    allowed_methods = [
        "get",  # 'post', 'put', 'delete'
    ]

    @extend_schema(
        responses={200: OpenApiTypes.OBJECT},
        parameters=[
            OpenApiParameter(
                name="kiinteistotunnus",
                type=str,
                location=OpenApiParameter.PATH,
                description="Experimental query for neighbours, kiinteistötunnus to get data for",
            ),
        ],
    )
    def get(self, request, *args, **kwargs):
        if not request.version:
            return HttpResponseBadRequest("Need version!")

        version = int(request.version)
        if "version" in kwargs:
            # Note: It's pretty sure the value is there, but let's have an if just to be sure.
            del kwargs["version"]
        if version == 1:
            api = APIv1(request=request)
            return api.get(request, *args, **kwargs)

        raise ValueError("Unknown version!")
