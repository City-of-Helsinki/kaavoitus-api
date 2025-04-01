from django.urls import path, re_path
from kaavapino_api import views

urlpatterns = [
    path("heartbeat", views.heartbeat.API.as_view(), name="heartbeat"),
    re_path(
        r"^v(?P<version>(1))/project/changes",
        views.project_change.API.as_view(),
        name="changes",
    ),
    re_path(
        r"^v(?P<version>(1))/project/(?P<pinonro>[^/]*)",
        views.project.API.as_view(),
        name="project",
    ),
    re_path(
        r"^v(?P<version>(1))/project/(?P<pinonro>[^/]*)/data",
        views.project.API.as_view(),
        name="project_data",
    ),
    re_path(
        r"^v(?P<version>(1))/project/(?P<pinonro>[^/]*)/trigger-change",
        views.project_trigger_change.API.as_view(),
        name="changes",
    ),
]
