from rest_framework.views import APIView  # pip install django-rest-framework
from django.http import HttpResponseBadRequest
import logging

log = logging.getLogger(__name__)


class API(APIView):
    def patch(self, request, pinonro=None):
        if not pinonro:
            return HttpResponseBadRequest("Need pinonro!")

        raise NotImplementedError("Not yet!")

        # Go validate the returned data.
        # It needs to be verifiable by serializer rules. Those are published in Swagger.
        # serializer = self.serializer_class(data=data)
        # if not serializer.is_valid():
        #     return HttpResponseServerError("Invalid data received from WFS!")

        # return JsonResponse(serializer.validated_data)
