from rest_framework.views import APIView  # pip install django-rest-framework
import logging
from kaavapino_api.views.serializers.v1 import ChangeV1Serializer

log = logging.getLogger(__name__)


class API(APIView):
    serializer_class = ChangeV1Serializer

    def get(self, request, timestamp=None):
        raise NotImplementedError("Not yet!")

        # Go validate the returned data.
        # It needs to be verifiable by serializer rules. Those are published in Swagger.
        # serializer = self.serializer_class(data=data)
        # if not serializer.is_valid():
        #     return HttpResponseServerError("Invalid data received from WFS!")

        # return JsonResponse(serializer.validated_data)
