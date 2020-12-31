from rest_framework.views import APIView  # pip install django-rest-framework
from rest_framework import versioning
from drf_spectacular.openapi import AutoSchema


class API(APIView):
    queryset = None
    schema = AutoSchema()
    versioning_class = versioning.URLPathVersioning

    def get_queryset(self):
        return None
