from setuptools import setup

setup(
    name="Kaavoitus-API",
    version="0.1.0",
    packages=[
        "facta_api",
        "api_project",
        "common_auth",
        "geoserver_api",
        "kaavapino_api",
    ],
    url="https://github.com/City-of-Helsinki/kaavoitus-api",
    license="",
    author="Helsingin Kaupunki",
    author_email="",
    description="Kaavoitus API",
    install_requires=[
        "django == 3.1.6",
        "django-environ ==  0.4.5",
        "djangorestframework == 3.12.2",
        "django-extensions == 3.1.1",
        "drf_spectacular == 0.13.2",
        "owslib == 0.22.0",
        "lxml == 4.6.2",
        "pydov == 2.0.0",
        "psycopg2 == 2.9.2",
        "cx_Oracle == 8.1.0",
        "gunicorn == 20.0.4",
        "numpy == 1.20.0",
        "geojson == 2.5.0",
        "GDAL >=3.0.0,<3.1",
        "sentry-sdk == 1.5.6",
    ],
    extras_require={
        "dev": [
            "black",
            "flake8",
            "flake8-print",
            "pytest",
            "pytest-cov",
            "pytest-django",
        ]
    },
)
