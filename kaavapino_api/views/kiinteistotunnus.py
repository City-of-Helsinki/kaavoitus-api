from rest_framework.views import APIView  # pip install django-rest-framework
from django.http import JsonResponse, HttpResponseBadRequest
from drf_spectacular.openapi import AutoSchema
from drf_spectacular.utils import extend_schema, OpenApiParameter
from drf_spectacular.types import OpenApiTypes
from .v1.kiinteistotunnus import API as APIv1
from .v2.kiinteistotunnus import API as APIv2


class API(APIView):
    allowed_methods = [
        'get', 'post'  # , 'put', 'delete'
    ]
    schema = AutoSchema(

    )

    @extend_schema(
        responses={200: OpenApiTypes.OBJECT},
        parameters=[
            OpenApiParameter(
                name='id',
                type=str,
                location=OpenApiParameter.PATH,
                description='Kiinteistötunnus to get data for',

            ),
            # extra parameters added to the schema
            OpenApiParameter(
                name='alue',
                type=str,
                location=OpenApiParameter.QUERY,
                description='Filter by alue',

            ),
        ],
        # override default docstring extraction
        description='Hae kiinteistö kiinteistötunnuksella',
        # provide Authentication class that deviates from the views default
        auth=None,
        # change the auto-generated operation name
        operation_id=None,
        # or even completely override what AutoSchema would generate. Provide raw Open API spec as Dict.
        operation=None,
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

        if version == 2:
            api = APIv2(request=request)
            return api.get(request, *args, **kwargs)

        raise ValueError("Unknown version!")

    @extend_schema(
        responses={200: OpenApiTypes.OBJECT},
        parameters=[
            # POST (create) doesn't even have this parameter, but it needs to be documented?
            OpenApiParameter(
                name='id',
                type=str,
                location=OpenApiParameter.PATH,
                description='Kiinteistötunnus to get data for',

            ),
        ],
    )
    def post(self, request):
        if not request.version:
            return HttpResponseBadRequest("Need version!")

        version = int(request.version)
        if version == 1:
            api = APIv1(request=request)
            return api.post(request)

        if version == 2:
            api = APIv2(request=request)
            return api.post(request)

        raise ValueError("Unknown version!")
