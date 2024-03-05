from unittest.mock import Mock

import pytest

from django.urls import reverse
from rest_framework.test import APIClient


class TestPaikkatieto:
    client = APIClient()

    def test_get_paikkatieto(self, f_token1):
        self.client.credentials(HTTP_AUTHORIZATION="Token " + f_token1.key)

        url = reverse(
            "hel:paikkatieto", kwargs={"version": 1, "hankenumero": "1234_56"}
        )
        response = self.client.get(url)

        assert response.status_code == 200

        assert response.json() == {
            'voimassa_asemakaavat': '',
            'voimassa_olevat_rakennuskiellot': '',
            'maanomistus_kaupunki': 'Ei',
            'maanomistus_valtio': 'Ei',
            'maanomistus_yksityinen': 'Ei',
            'maanomistaja_ulkopaikkakunta': 'Ei',
            'haltija_ulkopaikkakunta': 'Ei'
        }