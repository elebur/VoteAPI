import json

from rest_framework_simplejwt.tokens import RefreshToken


def de_json(text: str) -> dict:
    return json.loads(text)


def get_jwt_for_user(user):
    refresh = RefreshToken.for_user(user)
    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }
