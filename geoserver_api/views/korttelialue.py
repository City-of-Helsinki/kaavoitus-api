from rest_framework.views import APIView  # pip install django-rest-framework
from rest_framework import permissions
from django.http import HttpResponseBadRequest
from drf_spectacular.openapi import AutoSchema
from drf_spectacular.utils import extend_schema, OpenApiParameter
from drf_spectacular.types import OpenApiTypes
from common_auth.authentication import TokenAuthentication
from .v1.korttelialue import API as APIv1


class API(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]
    # serializer_class = KiinteistoSerializer

    allowed_methods = [
        "get",  # 'post'  # , 'put', 'delete'
    ]
    schema = AutoSchema()

    @extend_schema(
        responses={
            200: OpenApiTypes.OBJECT,
            401: OpenApiTypes.STR,
            500: OpenApiTypes.STR,
        },
        parameters=[
            OpenApiParameter(
                name="korttelinnumero",
                type=str,
                location=OpenApiParameter.PATH,
                description="Korttelinnumero to get data for",
            ),
        ],
        # override default docstring extraction
        description="Hae kortteli korttelinnumerolla",
        # provide Authentication class that deviates from the views default
        # auth=None,
        # change the auto-generated operation name
        # operation_id=None,
        # or even completely override what AutoSchema would generate. Provide raw Open API spec as Dict.
        # operation=None,
        # attach request/response examples to the operation.
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
