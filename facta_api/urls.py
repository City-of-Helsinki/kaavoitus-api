from django.urls import path, re_path
from facta_api import views

urlpatterns = [
    path("heartbeat", views.heartbeat.API.as_view(), name="heartbeat"),
    re_path(
        r"^v(?P<version>(1))/kiinteisto/omistajat/(?P<kiinteistotunnus>[^/]*)$",
        views.kiinteiston_omistajat.API.as_view(),
        name="kiinteiston-omistajat",
    ),
    re_path(
        r"^v(?P<version>(1))/kiinteisto/haltijat/(?P<kiinteistotunnus>[^/]*)$",
        views.kiinteiston_haltijat.API.as_view(),
        name="kiinteiston-haltijat",
    ),
    re_path(
        r"^v(?P<version>(1))/kiinteisto/(?P<kiinteistotunnus>[^/]*)/all$",
        views.kiinteisto_all.API.as_view(),
        name="kiinteisto-info",
    ),
    re_path(
        r"^v(?P<version>(1))/rakennus/omistajat/(?P<kiinteistotunnus>[^/]*)$",
        views.rakennuksen_omistajat.API.as_view(),
        name="rakennuksen-omistajat",
    ),
]
