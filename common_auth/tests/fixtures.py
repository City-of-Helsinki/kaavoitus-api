import pytest
from django.contrib.auth import get_user_model

from common_auth.models import (
    ExtAuthCred,
    Token,
)


@pytest.fixture(scope="session")
def f_user1(django_db_blocker):
    with django_db_blocker.unblock():
        return get_user_model().objects.create(
            username="test_1",
            email="test_1@example.com",
            first_name="First",
            last_name="Tester",
        )


@pytest.fixture(scope="session")
def f_user2(django_db_blocker):
    with django_db_blocker.unblock():
        return get_user_model().objects.create(
            username="test_2",
            email="test_2@example.com",
            first_name="Second",
            last_name="Tester",
        )


@pytest.fixture(scope="session")
def f_facta(django_db_blocker):
    with django_db_blocker.unblock():
        return ExtAuthCred.objects.create(
            system="Facta",
            cred_owner="Kaavapino",
            username="Kaavapino_test",
            credential="facta_test",
            host_spec="",
        )


@pytest.fixture(scope="session")
def f_geoserver(django_db_blocker):
    with django_db_blocker.unblock():
        return ExtAuthCred.objects.create(
            system="Geoserver",
            cred_owner="Kaavapino",
            username="Kaavapino_test",
            credential="geoserver_test",
            host_spec="",
        )


@pytest.fixture(scope="session")
def f_kaavapino(django_db_blocker):
    with django_db_blocker.unblock():
        return ExtAuthCred.objects.create(
            system="Kaavapino",
            cred_owner="Kaavapino",
            username="Kaavapino_test",
            credential="kaavapino_test",
            host_spec="",
        )


@pytest.fixture(scope="session")
def f_token1(django_db_blocker, f_user1, f_facta, f_geoserver, f_kaavapino):
    with django_db_blocker.unblock():
        return Token.objects.create(
            user=f_user1,
            key="11223344",
            access_facta=f_facta,
            access_geoserver=f_geoserver,
            access_kaavapino=f_kaavapino,
        )


@pytest.fixture(scope="session")
def f_token2(django_db_blocker, f_user2):
    with django_db_blocker.unblock():
        return Token.objects.create(
            user=f_user2,
            key="44333222111",
            access_facta=None,
            access_geoserver=None,
            access_kaavapino=None,
        )
