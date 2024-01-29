import pytest

from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework.test import APIClient


class TestPaikkatieto:
    client = APIClient()

    @pytest.mark.parametrize(
        "username, hankenumero",
        [
            ("kaavapino", "1234_56")
        ],
    )
    def test_get_paikkatieto(self, username, hankenumero):
        user = User.objects.get(username="kaavapino")
        assert user is not None

        self.client.credentials(HTTP_AUTHORIZATION="Token " + user.wasted_auth_token.key)
        url = reverse(
            "hel:paikkatieto", kwargs={"version": 1, "hankenumero": "1234_00"}
        )

        result = self.client.get(url)

        assert result.status_code == 200
