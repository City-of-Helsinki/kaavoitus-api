"""api_project URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include, re_path
from drf_spectacular.views import SpectacularAPIView, SpectacularRedocView, SpectacularSwaggerView
from geoserver_api import urls as geoserver_urls
from kaavapino_api import urls as kaavapino_urls
from facta_api import urls as facta_urls

urlpatterns = [
#    path('', DefaultSpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui-default'),
    path('admin/', admin.site.urls),
    path('api/facta/', include((facta_urls.urlpatterns, 'facta'))),
    path('api/geoserver/', include((geoserver_urls.urlpatterns, 'geoserver'))),
    path('api/kaavapino/', include((kaavapino_urls.urlpatterns, 'kaavapino'))),
    # OpenAPI 3 documentation with Swagger UI:
    re_path(
        r'^schema/v(?P<version>(\d+))/',
        SpectacularAPIView.as_view(),
        name='schema'
    ),
    re_path(
        r'^schema/swagger-ui/v(?P<version>(\d+))/',
        SpectacularSwaggerView.as_view(url_name='schema'),
        name='swagger-ui-versioned'
    ),
    re_path(
        r'^schema/redoc/v(?P<version>(\d+))/',
        SpectacularRedocView.as_view(url_name='schema'),
        name='redoc'
    ),
]
