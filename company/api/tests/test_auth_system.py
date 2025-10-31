import pytest
from rest_framework import status

from api.tests.tools import get_jwt_for_user


def test_obtaining_tokens(admin, client):
    payload = {
        "username": "admin",
        "password": "password",
    }

    resp = client.post("/api/token/", payload)

    assert "refresh" in resp.text
    assert "access" in resp.text


@pytest.mark.django_db
def test_wrong_credentials(client):
    payload = {
        "username": "wrong_user",
        "password": "wrong_password",
    }

    resp = client.post("/api/token/", payload)

    assert resp.status_code == status.HTTP_401_UNAUTHORIZED


def test_refresh_token(admin, client):
    jwt = get_jwt_for_user(admin)

    payload = {"refresh": jwt["refresh"]}

    resp = client.post("/api/token/refresh/", payload)

    assert "access" in resp.text
    assert "refresh" not in resp.text
