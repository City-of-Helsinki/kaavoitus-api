from django.urls import path, re_path
from hel_api import views

urlpatterns = [
    path("heartbeat", views.heartbeat.API.as_view(), name="heartbeat"),
    re_path(
        r"^v(?P<version>(1))/paikkatieto/(?P<hankenumero>[^/]*)$",
        views.paikkatieto.API.as_view(),
        name="paikkatieto",
    ),
]
