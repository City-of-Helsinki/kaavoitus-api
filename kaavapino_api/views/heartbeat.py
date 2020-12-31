from rest_framework.views import APIView  # pip install django-rest-framework
from django.http import JsonResponse, HttpResponseBadRequest
from drf_spectacular.openapi import AutoSchema
from drf_spectacular.utils import extend_schema, OpenApiParameter


class API(APIView):
    versioning_class = None
    allowed_methods = [
        'get'
    ]
    schema = AutoSchema()
    serializer_class = None

    @extend_schema(
        # override default docstring extraction
        description='Simple service is alive test',
        # provide Authentication class that deviates from the views default
        auth=None,
        # change the auto-generated operation name
        # operation_id=None,
        # or even completely override what AutoSchema would generate. Provide raw Open API spec as Dict.
        # operation=None,
        # attach request/response examples to the operation.

    )
    def get(self, request):
        if request.auth:
            retval = {'status': 'authenticated ok.'}
        else:
            retval = {'status': 'ok.'}

        return JsonResponse(retval, content_type="application/json")
