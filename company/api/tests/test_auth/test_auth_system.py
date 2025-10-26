from api.tests.tools import send_json

def test_obtaining_tokens(superuser, client):
    c = client

    payload = {
        "username": "admin",
        "password": "password"
    }

    resp = send_json(c, "/api/token/", payload)

    assert "refresh" in resp and "access" in resp


def test_refresh_token(superuser, client):
    payload = {
        "username": "admin",
        "password": "password"
    }
    resp_init = send_json(client, "/api/token/", payload)

    payload_refreshed = {
        "refresh": resp_init["refresh"]
    }
    refreshed = send_json(client, "/api/token/refresh/", payload_refreshed)

    assert "access" in refreshed
