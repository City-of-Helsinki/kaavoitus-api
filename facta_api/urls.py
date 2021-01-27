from django.urls import path, re_path
from rest_framework.versioning import URLPathVersioning
from facta_api import views

urlpatterns = [
    path('heartbeat',
         views.heartbeat.API.as_view(),
         name='heartbeat'),
    re_path(
        r'^v(?P<version>(1))/kiinteiston-omistajat/(?P<kiinteistotunnus>[^/]*)$',
        views.kiinteiston_omistajat.API.as_view(),
        name='kiinteiston-omistajat'
    ),
]
