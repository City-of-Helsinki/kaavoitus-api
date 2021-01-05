from django.urls import path, re_path
from rest_framework.versioning import URLPathVersioning
from kaavapino_api import views

urlpatterns = [
    # path('tontti', tontti.API.as_view(), name='tontti'),
    path('heartbeat',
         views.heartbeat.API.as_view(),
         name='heartbeat'),
    re_path(
        r'^v(?P<version>(1))/asemakaava_voimassa/(?P<id>[^/]*)',
        views.asemakaava_voimassa.API.as_view(),
        name='asemakaava-voimassa'
    ),
    re_path(
        r'^v(?P<version>(1|2))/kiinteistotunnus/(?P<id>[^/]*)',
        views.kiinteistotunnus.API.as_view(),
        name='kiinteistötunnus'
    ),
    re_path(
        r'^v(?P<version>(1))/maarekisterikiinteisto/(?P<id>[^/]*)',
        views.maarekisterikiinteisto.API.as_view(),
        name='maarekisterikiinteisto'
    ),
    re_path(
        r'^v(?P<version>(1))/rakennuskieltoalue_asemakaava/(?P<id>[^/]*)',
        views.rakennuskieltoalue_asemakaava.API.as_view(),
        name='rakennuskieltoalue_asemakaava'
    ),
    re_path(
        r'^v(?P<version>(1))/rakennuskieltoalue_yleiskaava/(?P<id>[^/]*)',
        views.rakennuskieltoalue_yleiskaava.API.as_view(),
        name='rakennuskieltoalue_yleiskaava'
    ),
    re_path(
        r'^v(?P<version>(1))/tontti/(?P<id>[^/]*)',
        views.tontti.API.as_view(),
        name='tontti'
    ),
    re_path(
        r'^v(?P<version>(1))/neighbourhood/(?P<id>[^/]*)',
        views.neighbourhood.API.as_view(),
        name='neighbourhood'
    ),
]
