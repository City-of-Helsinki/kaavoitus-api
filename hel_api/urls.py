from django.urls import path, re_path
from hel_api import views

urlpatterns = [
    path("heartbeat", views.heartbeat.API.as_view(), name="heartbeat"),
    re_path(
        r"^v(?P<version>(1))/paikkatieto/(?P<hankenumero>[^/]*)$",
        views.paikkatieto.API.as_view(),
        name="paikkatieto",
    ),
    re_path(
        r"^v(?P<version>(1))/kiinteistotunnukset/(?P<hankenumero>[^/]*)$",
        views.kiinteistotunnukset.API.as_view(),
        name="kiinteistotunnukset",
    ),
    re_path(
        r"^v(?P<version>(1))/rakennuskiellot/(?P<hankenumero>[^/]*)$",
        views.rakennuskiellot.API.as_view(),
        name="rakennuskiellot",
    ),
    re_path(
        r"^v(?P<version>(1))/kaavat/(?P<hankenumero>[^/]*)$",
        views.kaavat.API.as_view(),
        name="kaavat",
    ),
]
