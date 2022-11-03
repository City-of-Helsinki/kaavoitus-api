"""
Django settings for api_project project.

Generated by 'django-admin startproject' using Django 3.1.4.

For more information on this file, see
https://docs.djangoproject.com/en/3.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.1/ref/settings/
"""

import os
import environ
from pathlib import Path
import logging

import sentry_sdk
from sentry_sdk.integrations.django import DjangoIntegration

logger = logging.getLogger(__name__)

CONFIG_FILE_NAME = "config_dev.env"

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

root = environ.Path(__file__) - 1  # one level back in hierarchy
env = environ.Env(
    DATABASE_URL=(str, "sqlite:///" + str(BASE_DIR / "db/db.sqlite3")),
    KEYDB_URL=(str, "redis://localhost:6379/1"),
    DEBUG=(bool, False),
    LANGUAGES=(list, ["fi", "sv", "en"]),
    SECRET_KEY=(str, None),
    ALLOWED_HOSTS=(list, []),
    LOG_LEVEL=(str, "WARNING"),
    FACTA_DB_MOCK_DATA_DIR=(str, None),
    USE_JSON_READER=(bool, True),
    KAAVAPINO_API_URL=(str, None),
    SENTRY_DSN=(str, ''),
    SENTRY_ENVIRONMENT=(str, 'development'),
    ELASTIC_APM_SERVER_URL=(str, ""),
    ELASTIC_APM_SERVICE_NAME=(str, ""),
    ELASTIC_APM_SECRET_TOKEN=(str, ""),
)


if env.str("ELASTIC_APM_SERVER_URL"):
    ELASTIC_APM = {
        "DEBUG": True,
        "SERVER_URL": env.str("ELASTIC_APM_SERVER_URL"),
        "SERVICE_NAME": env.str("ELASTIC_APM_SERVICE_NAME"),
        "SECRET_TOKEN": env.str("ELASTIC_APM_SECRET_TOKEN"),
    }


if env('SENTRY_DSN'):
    sentry_sdk.init(
        dsn=env('SENTRY_DSN'),
        environment=env('SENTRY_ENVIRONMENT'),
        integrations=[DjangoIntegration()]
    )


# Django environ has a nasty habit of complaining at level
# WARN about env file not being preset. Here we pre-empt it.
env_file_path = os.path.join(BASE_DIR, CONFIG_FILE_NAME)
if os.path.exists(env_file_path):
    # Logging configuration is not available at this point
    print(f"Reading config from {env_file_path}")  # noqa: T001
    environ.Env.read_env(env_file_path)

DEBUG = env("DEBUG")
ALLOWED_HOSTS = env("ALLOWED_HOSTS")

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.1/howto/deployment/checklist/

# If a secret key was not supplied elsewhere, generate a random one and log
# a warning (note that logging is not configured yet). This means that any
# functionality expecting SECRET_KEY to stay same will break upon restart.
# Should not be a problem for development.
if "SECRET_KEY" not in locals():
    logger.warning(
        "SECRET_KEY was not defined in configuration. Generating an ephemeral key."
    )
    import random

    system_random = random.SystemRandom()
    SECRET_KEY = "".join(
        [
            system_random.choice("abcdefghijklmnopqrstuvwxyz0123456789!@#$%^&*(-_=+)")
            for i in range(64)
        ]
    )

# Application definition

INSTALLED_APPS = [
    # Own:
    "common_auth",
    "facta_api",
    "geoserver_api",
    "kaavapino_api",
    # Django:
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    # Added Django libs:
    "rest_framework",
    "django_extensions",  # pip install django-extensions
    "drf_spectacular",  # pip install drf-spectacular
]

if env.str("ELASTIC_APM_SERVER_URL"):
    INSTALLED_APPS += ["elasticapm.contrib.django"]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "api_project.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "api_project.wsgi.application"

# Database
# https://docs.djangoproject.com/en/3.1/ref/settings/#databases

DATABASES = {
    "default": env.db()
}

# Cache can be disabled by setting timeout to 0. Warning: Timeout of 'None' will cache data forever.
# Key value pairs can be cleared from cache by using keydb-cli: Select the correct database and run 'flushdb'
FACTA_CACHE_TIMEOUT = 60 * 60 * 1  # 1 hour
GEOSERVER_CACHE_TIMEOUT = 60 * 60 * 1  # 1 hour

CACHES = {
    "default": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": env.str("KEYDB_URL"),
        "OPTIONS": {"CLIENT_CLASS": "django_redis.client.DefaultClient"},
        "KEY_PREFIX": "kaavoitus_api",
    }
}

# Password validation
# https://docs.djangoproject.com/en/3.1/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]

# Internationalization
# https://docs.djangoproject.com/en/3.1/topics/i18n/

LANGUAGE_CODE = "en-us"

TIME_ZONE = "UTC"

USE_I18N = True

USE_L10N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.1/howto/static-files/

STATIC_URL = "/static/"

REST_FRAMEWORK = {
    "DEFAULT_AUTHENTICATION_CLASSES": [
        "common_auth.authentication.TokenAuthentication",
    ],
    "DEFAULT_VERSIONING_CLASS": "rest_framework.versioning.URLPathVersioning",
    "DEFAULT_SCHEMA_CLASS": "drf_spectacular.openapi.AutoSchema",
    # Note: Would love to use, but crashes with error on HTTP-request to retrieve schema.
    # 'drf_spectacular.openapi.AutoSchema',
    # Works:
    # 'rest_framework.schemas.coreapi.AutoSchema',
    "ALLOWED_VERSIONS": ["1", "2"],
}

SPECTACULAR_SETTINGS = {
    # path prefix is used for tagging the discovered operations.
    # use '/api/v[0-9]' for tagging apis like '/api/v1/albums' with ['albums']
    "SCHEMA_PATH_PREFIX": r"^/api/",
    "DEFAULT_GENERATOR_CLASS": "drf_spectacular.generators.SchemaGenerator",
    # Schema generation parameters to influence how components are constructed.
    # Some schema features might not translate well to your target.
    # Demultiplexing/modifying components might help alleviate those issues.
    #
    # Create separate components for PATCH endpoints (without required list)
    "COMPONENT_SPLIT_PATCH": True,
    # Split components into request and response parts where appropriate
    "COMPONENT_SPLIT_REQUEST": False,
    # Aid client generator targets that have trouble with read-only properties.
    "COMPONENT_NO_READ_ONLY_REQUIRED": False,
    # Configuration for serving the schema with SpectacularAPIView
    "SERVE_URLCONF": None,
    # complete public schema or a subset based on the requesting user
    "SERVE_PUBLIC": True,
    # is the
    "SERVE_INCLUDE_SCHEMA": True,
    "SERVE_PERMISSIONS": ["rest_framework.permissions.AllowAny"],
    # Dictionary of configurations to pass to the SwaggerUI({ ... })
    # https://swagger.io/docs/open-source-tools/swagger-ui/usage/configuration/
    "SWAGGER_UI_SETTINGS": {
        "deepLinking": True,
    },
    "SWAGGER_UI_DIST": "//unpkg.com/swagger-ui-dist@3.35.1",
    "SWAGGER_UI_FAVICON_HREF": "//unpkg.com/swagger-ui-dist@3.35.1/favicon-32x32.png",
    # Append OpenAPI objects to path and components in addition to the generated objects
    "APPEND_PATHS": {},
    "APPEND_COMPONENTS": {},
    # DISCOURAGED - please don't use this anymore as it has tricky implications that
    # are hard to get right. For authentication, OpenApiAuthenticationExtension are
    # strongly preferred because they are more robust and easy to write.
    # However if used, the list of methods is appended to every endpoint in the schema!
    "SECURITY": [],
    # Postprocessing functions that run at the end of schema generation.
    # must satisfy interface result = hook(generator, request, public, result)
    "POSTPROCESSING_HOOKS": ["drf_spectacular.hooks.postprocess_schema_enums"],
    # Preprocessing functions that run before schema generation.
    # must satisfy interface result = hook(endpoints=result) where result
    # is a list of Tuples (path, path_regex, method, callback).
    # Example: 'drf_spectacular.hooks.preprocess_exclude_path_format'
    "PREPROCESSING_HOOKS": [],
    # enum name overrides. dict with keys "YourEnum" and their choice values "field.choices"
    "ENUM_NAME_OVERRIDES": {},
    # Adds "blank" and "null" enum choices where appropriate. disable on client generation issues
    "ENUM_ADD_EXPLICIT_BLANK_NULL_CHOICE": True,
    # function that returns a list of all classes that should be excluded from doc string extraction
    "GET_LIB_DOC_EXCLUDES": "drf_spectacular.plumbing.get_lib_doc_excludes",
    # Function that returns a mocked request for view processing. For CLI usage
    # original_request will be None.
    # interface: request = build_mock_request(method, path, view, original_request, **kwargs)
    "GET_MOCK_REQUEST": "drf_spectacular.plumbing.build_mock_request",
    # Camelize names like operationId and path parameter names
    "CAMELIZE_NAMES": False,
    # General schema metadata. Refer to spec for valid inputs
    # https://github.com/OAI/OpenAPI-Specification/blob/master/versions/3.0.3.md#openapi-object
    "TITLE": "Helsingin Kaupunki - Kaavoitus-API",
    "DESCRIPTION": "Kaavoitus-API for Facta and Geoserver data",
    "TOS": None,
    # Optional: MAY contain "name", "url", "email"
    "CONTACT": {},
    # Optional: MUST contain "name", MAY contain URL
    "LICENSE": {},
    "VERSION": "1.0.0",
    # Optional list of servers.
    # Each entry MUST contain "url", MAY contain "description", "variables"
    "SERVERS": [],
    # Tags defined in the global scope
    "TAGS": [],
    # Optional: MUST contain 'url', may contain "description"
    "EXTERNAL_DOCS": {},
    # Oauth2 related settings. used for example by django-oauth2-toolkit.
    # https://github.com/OAI/OpenAPI-Specification/blob/master/versions/3.0.3.md#oauth-flows-object
    "OAUTH2_FLOWS": [],
    "OAUTH2_AUTHORIZATION_URL": None,
    "OAUTH2_TOKEN_URL": None,
    "OAUTH2_REFRESH_URL": None,
    "OAUTH2_SCOPES": None,
}

LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
        },
    },
    "root": {
        "handlers": ["console"],
        "level": env("LOG_LEVEL"),
    },
}

FACTA_DB_MOCK_DATA_DIR = env("FACTA_DB_MOCK_DATA_DIR")

USE_JSON_READER = env("USE_JSON_READER")

KAAVAPINO_API_URL = env("KAAVAPINO_API_URL")

