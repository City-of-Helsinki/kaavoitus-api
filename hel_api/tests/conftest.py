import pytest

from api_project import settings


@pytest.fixture(scope='session')
def django_db_setup():
    settings.DATABASES['default'] = settings.env.db()
