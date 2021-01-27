from setuptools import setup

setup(
    name='Kaavoitus-API',
    version='0.1.0',
    packages=['facta_api',
              'api_project',
              'common_auth',
              'geoserver_api',
              'kaavapino_api',
              ],
    url='https://github.com/City-of-Helsinki/kaavoitus-api',
    license='',
    author='Helsingin Kaupunki',
    author_email='',
    description='Kaavoitus API',
    install_requires=[
        'django',
        'django-environ',
        'djangorestframework',
        'django-extensions',
        'drf_spectacular',
        'owslib',
        'lxml',
        'pydov',
        'cx_Oracle',
    ]
)
