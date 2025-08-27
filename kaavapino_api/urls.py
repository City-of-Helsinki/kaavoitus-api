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
        r"^v(?P<version>(1))/projects/attribute_data",
        views.projects_attribute_data.API.as_view(),
        name="projects_attribute_data",
    ),
    re_path(
        r"^v(?P<version>(1))/project/(?P<pinonro>[^/]*)/trigger-change",
        views.project_trigger_change.API.as_view(),
        name="changes",
    ),
]
