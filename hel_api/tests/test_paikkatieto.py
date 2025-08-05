from unittest.mock import Mock

import pytest

from django.urls import reverse
from rest_framework.test import APIClient


class TestPaikkatieto:
    client = APIClient()

    @pytest.mark.django_db
    def test_get_paikkatieto(self, f_token1):
        from hel_api.views.v1.kiinteistotunnukset import API as KiinteistoAPI
        from hel_api.views.v1.maaraalatunnukset import API as MaaraalaAPI
        from hel_api.views.v1.kaavat import API as KaavaAPI
        from hel_api.views.v1.rakennuskiellot import API as RakennuskieltoAPI

        self.client.credentials(HTTP_AUTHORIZATION="Token " + f_token1.key)

        k_api = KiinteistoAPI
        m_api = MaaraalaAPI
        kaava_api = KaavaAPI
        rakennuskielto_api = RakennuskieltoAPI

        k_api.get_data = Mock(return_value={"hankenumero": "1234_56", "kiinteistotunnukset": []})
        m_api.get_data = Mock(return_value={"hankenumero": "1234_56", "maaraalatunnukset": []})
        kaava_api.get_data = Mock(return_value={"hankenumero": "1234_56", "kaavat": []})
        rakennuskielto_api.get_data = Mock(return_value={"hankenumero": "1234_56", "rakennuskiellot": []})

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