from rest_framework.views import APIView  # pip install django-rest-framework
from django.http import JsonResponse
from drf_spectacular.openapi import AutoSchema
from drf_spectacular.utils import extend_schema
from drf_spectacular.types import OpenApiTypes


class API(APIView):
    # No auth nor permissions required for this. Will remove lock-icon in Swagger.
    authentication_classes = []
    permission_classes = []
    # Not versioned.
    versioning_class = None
    allowed_methods = ["get"]
    schema = AutoSchema()
    serializer_class = None

    @extend_schema(
        responses={
            200: OpenApiTypes.OBJECT,
            500: OpenApiTypes.OBJECT,
        },
        # override default docstring extraction
        description="Simple service is alive test",
        # provide Authentication class that deviates from the views default
        auth=None,
        # change the auto-generated operation name
        operation_id=None,
        # or even completely override what AutoSchema would generate. Provide raw Open API spec as Dict.
        operation=None,
        # attach request/response examples to the operation.
    )
    def get(self, request):
        if request.auth:
            retval = {"status": "authenticated ok."}
        else:
            retval = {"status": "ok."}

        return JsonResponse(retval)
