from rest_framework.views import APIView  # pip install django-rest-framework
from django.http import JsonResponse, HttpResponseBadRequest
from drf_spectacular.utils import extend_schema
from drf_spectacular.types import OpenApiTypes


class API(APIView):
    def get(self, request, id=None):
        if not id:
            return HttpResponseBadRequest("Need id!")
        retval = {"ping": "pong v2"}

        return JsonResponse(retval, content_type="application/json")

    @extend_schema(responses={200: OpenApiTypes.OBJECT})
    def post(self, request):
        pass

    def get_queryset(self):
        return None
