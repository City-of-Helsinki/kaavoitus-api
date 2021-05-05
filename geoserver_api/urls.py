from django.urls import path, re_path
from geoserver_api import views

urlpatterns = [
    # path('tontti', tontti.API.as_view(), name='tontti'),
    path("heartbeat", views.heartbeat.API.as_view(), name="heartbeat"),
    re_path(
        r"^v(?P<version>(1))/asemakaava/(?P<kaavatunnus>[^/]*)$",
        views.asemakaava.API.as_view(),
        name="asemakaava",
    ),
    re_path(
        r"^v(?P<version>(1))/asemakaava/(?P<kiinteistotunnus>[^/]*)/voimassa",
        views.asemakaava_voimassa.API.as_view(),
        name="asemakaava-voimassa",
    ),
    re_path(
        r"^v(?P<version>(1))/asemakaava/(?P<kiinteistotunnus>[^/]*)/kaavamaarays",
        views.kaavamaarays.API.as_view(),
        name="asemakaava-maaraus",
    ),
    re_path(
        r"^v(?P<version>(1|2))/kiinteisto/(?P<kiinteistotunnus>[^/]*)$",
        views.kiinteisto.API.as_view(),
        name="kiinteistötunnus",
    ),
    re_path(
        r"^v(?P<version>(1))/kiinteisto/(?P<kiinteistotunnus>[^/]*)/all$",
        views.kiinteisto_all.API.as_view(),
        name="kiinteistötunnus",
    ),
    re_path(
        r"^v(?P<version>(1))/maarekisterikiinteisto/(?P<kiinteistotunnus>[^/]*)",
        views.maarekisterikiinteisto.API.as_view(),
        name="maarekisterikiinteisto",
    ),
    re_path(
        r"^v(?P<version>(1))/rakennuskieltoalue/asemakaava/(?P<kiinteistotunnus>[^/]*)",
        views.rakennuskieltoalue_asemakaava.API.as_view(),
        name="rakennuskieltoalue_asemakaava",
    ),
    re_path(
        r"^v(?P<version>(1))/rakennuskieltoalue/yleiskaava/(?P<kiinteistotunnus>[^/]*)",
        views.rakennuskieltoalue_yleiskaava.API.as_view(),
        name="rakennuskieltoalue_yleiskaava",
    ),
    re_path(
        r"^v(?P<version>(1))/tontti/(?P<kiinteistotunnus>[^/]*)",
        views.tontti.API.as_view(),
        name="tontti",
    ),
    re_path(
        r"^v(?P<version>(1))/korttelialue/(?P<korttelinnumero>[^/]*)",
        views.korttelialue.API.as_view(),
        name="tontti",
    ),
    re_path(
        r"^v(?P<version>(1))/rakennusala/(?P<kiinteistotunnus>[^/]*)",
        views.rakennusala.API.as_view(),
        name="tontti",
    ),
    re_path(
        r"^v(?P<version>(1))/ymparistoalue/(?P<kiinteistotunnus>[^/]*)",
        views.ymparistoalue.API.as_view(),
        name="tontti",
    ),
    re_path(
        r"^v(?P<version>(1))/neighbourhood/(?P<kiinteistotunnus>[^/]*)",
        views.neighbourhood.API.as_view(),
        name="neighbourhood",
    ),
    re_path(
        r"^v(?P<version>(1))/suunnittelualue/(?P<hankenumero>[^/]*)",
        views.suunnittelualue.API.as_view(),
        name="suunnittelualue",
    ),
    re_path(
        r"^v(?P<version>(1))/kiinteistot/(?P<hankenumero>[^/]*)",
        views.kiinteistot.API.as_view(),
        name="kiinteistot",
    ),
]
