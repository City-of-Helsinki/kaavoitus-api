from rest_framework.authentication import (
    TokenAuthentication as Django_TokenAuthentication,
)
from common_auth.models.token_auth import Token


class TokenAuthentication(Django_TokenAuthentication):
    model = Token
