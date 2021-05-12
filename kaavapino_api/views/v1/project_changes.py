from django.http.response import (
    HttpResponseForbidden,
    HttpResponseServerError,
    JsonResponse,
)
from rest_framework.views import APIView  # pip install django-rest-framework
from django.http import (
    HttpResponse,
    HttpResponseBadRequest,
)
import logging
from kaavapino_api.views.serializers.v1 import ProjectChangesV1Serializer
from kaavapino_api.kaavapino.kaavapino_client import KaavapinoClient

log = logging.getLogger(__name__)


class API(APIView):
    serializer_class = ProjectChangesV1Serializer

    def get(self, request):
        timestamp = request.GET.get("timestamp", None)
        if not timestamp:
            return HttpResponseBadRequest("Need timestamp!")

        if not request.auth:
            return HttpResponse(status=401)

        kaavapino_creds = request.auth.access_kaavapino
        if not kaavapino_creds:
            return HttpResponseForbidden("No access!")

        self.client = KaavapinoClient(api_key=kaavapino_creds.credential)

        # Fetch projects changes from kaavopino
        projects_changes = self.client.get_projects_changes(timestamp)

        # Go validate the returned data.
        # It needs to be verifiable by serializer rules. Those are published in Swagger.
        serializer = self.serializer_class(data=projects_changes)
        if not serializer.is_valid():
            return HttpResponseServerError("Invalid data received from Kaavapino!")

        return JsonResponse(serializer.validated_data)
