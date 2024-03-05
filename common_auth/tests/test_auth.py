from django.urls import reverse
from rest_framework.test import APIClient
from unittest.mock import Mock

from common_auth.tests.mock import OracleConnMock
from kaavapino_api.kaavapino.kaavapino_client import KaavapinoClient
from geoserver_api.hki_geoserver.abstract.geoserver_reader import GeoServer_Reader

import pytest

class TestAuthentication:
    client = APIClient()

    def test_user__no_auth(self):
        url = reverse(
            "geoserver:suunnittelualue", kwargs={"version": 1, "hankenumero": 1}
        )

        response = self.client.get(url)

        assert response.status_code == 401

    def test_user__cannot_access_facta__kiinteisto_info(self, f_token2):
        self.client.credentials(HTTP_AUTHORIZATION="Token " + f_token2.key)
        url = reverse(
            "facta:kiinteisto-info",
            kwargs={"version": 1, "kiinteistotunnus": 12345678901234},
        )

        response = self.client.get(url)

        assert response.status_code == 403

    @pytest.mark.django_db
    def test_user__can_access_facta__kiinteisto_info(self, f_token1):
        from facta_api.hel_facta.abstract.facta import Facta

        self.client.credentials(HTTP_AUTHORIZATION="Token " + f_token1.key)
        url = reverse(
            "facta:kiinteisto-info",
            kwargs={"version": 1, "kiinteistotunnus": 12345678901234},
        )

        facta = Facta
        facta.__init__ = Mock(return_value=None)
        facta.conn = OracleConnMock

        reader = GeoServer_Reader
        reader.query = Mock(return_value=(0, {}))

        response = self.client.get(url)

        assert response.status_code == 404

    def test_user__cannot_access_geoserver__kiinteistot(self, f_token2):
        self.client.credentials(HTTP_AUTHORIZATION="Token " + f_token2.key)
        url = reverse("geoserver:kiinteistot", kwargs={"version": 1, "hankenumero": 1})

        response = self.client.get(url)

        assert response.status_code == 403

    def test_user__can_access_geoserver__kiinteistot(self, f_token1):
        self.client.credentials(HTTP_AUTHORIZATION="Token " + f_token1.key)
        url = reverse("geoserver:kiinteistot", kwargs={"version": 1, "hankenumero": 1})

        reader = GeoServer_Reader
        reader.query = Mock(return_value=(0, {}))

        response = self.client.get(url)

        assert response.status_code == 404

    def test_user__cannot_access_geoserver__suunnittelualue(self, f_token2):
        self.client.credentials(HTTP_AUTHORIZATION="Token " + f_token2.key)
        url = reverse(
            "geoserver:suunnittelualue", kwargs={"version": 1, "hankenumero": 1}
        )

        response = self.client.get(url)

        assert response.status_code == 403

    def test_user__can_access_geoserver__suunnittelualue(self, f_token1):
        self.client.credentials(HTTP_AUTHORIZATION="Token " + f_token1.key)
        url = reverse(
            "geoserver:suunnittelualue", kwargs={"version": 1, "hankenumero": 1}
        )

        reader = GeoServer_Reader
        reader.query = Mock(return_value=(0, {}))

        response = self.client.get(url)

        assert response.status_code == 404

    def test_user__cannot_access_kaavapino__project(self, f_token2):
        self.client.credentials(HTTP_AUTHORIZATION="Token " + f_token2.key)
        url = reverse("kaavapino:project", kwargs={"version": 1, "pinonro": 1})

        response = self.client.get(url)

        assert response.status_code == 403

    def test_user__can_access_kaavapino__project(self, f_token1):
        self.client.credentials(HTTP_AUTHORIZATION="Token " + f_token1.key)
        url = reverse("kaavapino:project", kwargs={"version": 1, "pinonro": 1})

        client = KaavapinoClient
        client.__init__ = Mock(return_value=None)
        client._get = Mock(return_value={})

        response = self.client.get(url)

        assert response.status_code == 404
