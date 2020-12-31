from rest_framework.views import APIView  # pip install django-rest-framework
from django.http import JsonResponse, HttpResponseBadRequest
from drf_spectacular.openapi import AutoSchema
from drf_spectacular.utils import extend_schema, OpenApiParameter
from drf_spectacular.types import OpenApiTypes
from .v1.maarekisterikiinteisto import API as APIv1


class API(APIView):
    schema = AutoSchema()
    allowed_methods = [
        'get',  # 'post', 'put', 'delete'
    ]

    @extend_schema(
        responses={200: OpenApiTypes.OBJECT},
        parameters=[
            OpenApiParameter(
                name='id',
                type=str,
                location=OpenApiParameter.PATH,
                description='Kiinteistötunnus to get data for',

            ),
        ],
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
