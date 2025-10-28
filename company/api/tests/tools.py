import json

from rest_framework.test import APIClient
from rest_framework_simplejwt.tokens import RefreshToken

PERMISSION_ERROR_403 = '{"detail":"You do not have permission to perform this action."}'
AUTH_REQUIRED_401 = '{"detail":"Authentication credentials were not provided."}'


def de_json(text: str) -> dict:
    return json.loads(text)


def get_jwt_for_user(user):
    refresh = RefreshToken.for_user(user)
    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }

def auth_client(client, jwt) -> APIClient:
    client.credentials(HTTP_AUTHORIZATION="Bearer "+ jwt["access"])

    return client
