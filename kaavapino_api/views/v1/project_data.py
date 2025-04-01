from django.http.response import (
    HttpResponseForbidden
)
from rest_framework.views import APIView  # pip install django-rest-framework
from django.http import (
    HttpResponse,
    HttpResponseBadRequest,
)
import logging
from kaavapino_api.views.serializers.v1 import ProjectV1Serializer
from kaavapino_api.kaavapino.kaavapino_client import KaavapinoClient

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

        project_data = self.client.get_projects_filtered(pinonro)

        return HttpResponse(project_data)
