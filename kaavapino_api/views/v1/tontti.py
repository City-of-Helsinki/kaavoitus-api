from rest_framework.views import APIView  # pip install django-rest-framework
from rest_framework import versioning
from django.http import JsonResponse, HttpResponseBadRequest
from drf_spectacular.openapi import AutoSchema


class API(APIView):
    api_version = 1
    schema = AutoSchema()
    versioning_class = versioning.URLPathVersioning
    allowed_methods = [
        'get', #'post', 'put', 'delete'
    ]

    def get_queryset(self):
        return None

    def get(self, request, id=None):
        if not id:
            return HttpResponseBadRequest("Need id!")
        retval = {'ping tontti': 'pong tontti'}

        return JsonResponse(retval, content_type="application/json")
