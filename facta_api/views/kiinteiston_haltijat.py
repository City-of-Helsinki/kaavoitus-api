from rest_framework.views import APIView  # pip install django-rest-framework
from rest_framework import authentication, permissions
from django.http import JsonResponse, HttpResponseBadRequest
from drf_spectacular.openapi import AutoSchema
from drf_spectacular.utils import extend_schema, OpenApiParameter
from drf_spectacular.types import OpenApiTypes
from common_auth.authentication import TokenAuthentication
from .v1.kiinteiston_haltijat import API as APIv1
from .serializers.v1 import KiinteistonHaltijatV1Serializer


class API(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    allowed_methods = [
        'get',
    ]
    schema = AutoSchema(

    )

    @extend_schema(
        responses={
            200: KiinteistonHaltijatV1Serializer,
            401: OpenApiTypes.STR,
            500: OpenApiTypes.STR,
        },
        parameters=[
            OpenApiParameter(
                name='kiinteistotunnus',
                type=str,
                location=OpenApiParameter.PATH,
                description='Kiinteistötunnus to get data for',

            ),
        ],
        # override default docstring extraction
        description='Hae kiinteistön haltijat kiinteistötunnuksella',
        # provide Authentication class that deviates from the views default
        #auth=None,
        # change the auto-generated operation name
        #operation_id=None,
        # or even completely override what AutoSchema would generate. Provide raw Open API spec as Dict.
        #operation=None,
        # attach request/response examples to the operation.

    )
    def get(self, request, *args, **kwargs):
        if not request.version:
            return HttpResponseBadRequest("Need version!")

        version = int(request.version)
        if 'version' in kwargs:
            # Note: It's pretty sure the value is there, but let's have an if just to be sure.
            del kwargs['version']
        if version == 1:
            api = APIv1(request=request)
            return api.get(request, *args, **kwargs)

        raise ValueError("Unknown version!")
