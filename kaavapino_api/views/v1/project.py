from django.http.response import (
    HttpResponseForbidden,
    HttpResponseNotFound,
    HttpResponseServerError,
    JsonResponse,
)
from rest_framework.views import APIView  # pip install django-rest-framework
from django.http import (
    HttpResponse,
    HttpResponseBadRequest,
)
import logging
from kaavapino_api.views.serializers.v1 import ProjectV1Serializer
from kaavapino_api.kaavapino.kaavapino_client import KaavapinoClient
from api_project.helpers import format_rich_text

log = logging.getLogger(__name__)


class API(APIView):
    serializer_class = ProjectV1Serializer

    def get(self, request, pinonro=None):
        if not pinonro:
            return HttpResponseBadRequest("Need pinonro!")

        if not request.auth:
            return HttpResponse(status=401)

        kaavapino_creds = request.auth.access_kaavapino
        if not kaavapino_creds:
            return HttpResponseForbidden("No access!")

        self.client = KaavapinoClient(api_key=kaavapino_creds.credential)

        # Fetch project data from kaavopino
        project_data = self.client.get_projects(pinonro)
        # log.info(project_data)
        attribute_data = project_data.get("attribute_data", {})
        if not attribute_data:
            return HttpResponseNotFound()

        data = attribute_data.copy()
        data["pinonumero"] = project_data.get("pino_number")
        data["suunnittelualueen_kuvaus"] = format_rich_text(data.get("suunnittelualueen_kuvaus"))

        # Go validate the returned data.
        # It needs to be verifiable by serializer rules. Those are published in Swagger.
        serializer = self.serializer_class(data=data)
        if not serializer.is_valid():
            return HttpResponseServerError("Invalid data received from Kaavapino")

        return JsonResponse(serializer.validated_data)
