from types import MappingProxyType

import pytest
from rest_framework.status import (
    HTTP_200_OK,
    HTTP_201_CREATED,
    HTTP_400_BAD_REQUEST,
    HTTP_401_UNAUTHORIZED,
    HTTP_403_FORBIDDEN,
    HTTP_404_NOT_FOUND,
)

from api.tests.tools import (
    AUTH_REQUIRED_401,
    PERMISSION_ERROR_403,
    auth_client,
    get_jwt_for_user,
)

PAYLOAD = MappingProxyType({
    "name": "RESTaurant's name",
    "username": "restaurant_user",
    "password": "password",
    "email": "restaurant@mail.com",
})

ENDPOINT = "/api/restaurant/"


def test_create_by_admin(admin, client):
    client = auth_client(client, get_jwt_for_user(admin))

    resp = client.post(ENDPOINT, PAYLOAD)

    assert resp.text == '{"restaurant_id":1}'
    assert resp.status_code == HTTP_201_CREATED


def test_create_by_user(user, client):
    client = auth_client(client, get_jwt_for_user(user))

    resp = client.post(ENDPOINT, PAYLOAD)

    assert resp.status_code == HTTP_403_FORBIDDEN
    assert resp.text == PERMISSION_ERROR_403


def test_create_by_anonymous(client):
    resp = client.post(ENDPOINT, PAYLOAD)

    assert resp.status_code == HTTP_401_UNAUTHORIZED
    assert resp.text == AUTH_REQUIRED_401


def test_create_with_duplicated_restaurant_name(client, admin):
    """Duplicated names for restaurants are allowed."""
    client = auth_client(client, get_jwt_for_user(admin))

    client.post(ENDPOINT, PAYLOAD)
    payload_copy = PAYLOAD.copy()
    payload_copy["username"] = "new_username"
    resp_duplicate = client.post(ENDPOINT, payload_copy)

    assert resp_duplicate.text == '{"restaurant_id":2}'
    assert resp_duplicate.status_code == HTTP_201_CREATED


def test_create_with_duplicated_username(client, admin):
    client = auth_client(client, get_jwt_for_user(admin))

    client.post(ENDPOINT, PAYLOAD)
    resp_duplicate = client.post(ENDPOINT, PAYLOAD)

    assert resp_duplicate.text == ('{"details":"The username '
                                   '\'restaurant_user\' is already in use"}')
    assert resp_duplicate.status_code == HTTP_400_BAD_REQUEST



def test_without_name_in_body(client, admin):
    client = auth_client(client, get_jwt_for_user(admin))

    payload = PAYLOAD.copy()
    payload.pop("name")
    payload["day"] = "Monday"
    resp = client.post(ENDPOINT, payload)

    assert resp.status_code == HTTP_400_BAD_REQUEST
    assert resp.text == '{"details":{"name":["This field is required."]}}'


@pytest.mark.freeze_time("2025-10-26T14:00:00")
def test_retrieve_by_admin(client, admin, restaurant):
    client = auth_client(client, get_jwt_for_user(admin))

    resp = client.get(ENDPOINT + f"{restaurant.id}/")

    assert resp.status_code == HTTP_200_OK
    assert resp.text == ('{"id":1,"name":"Restaurant",'
                         '"date_joined":"2025-10-26T14:00:00Z"}')


@pytest.mark.freeze_time("2025-10-26T14:00:00")
def test_retrieve_by_user(client, user, restaurant):
    client = auth_client(client, get_jwt_for_user(user))

    resp = client.get(ENDPOINT + f"{restaurant.id}/")

    assert resp.status_code == HTTP_200_OK
    assert resp.text == ('{"id":1,"name":"Restaurant",'
                         '"date_joined":"2025-10-26T14:00:00Z"}')


@pytest.mark.freeze_time("2025-10-26T14:00:00")
def test_retrieve_by_anonymous(client, restaurant):

    resp = client.get(ENDPOINT + f"{restaurant.id}/")

    assert resp.status_code == HTTP_200_OK
    assert resp.text == ('{"id":1,"name":"Restaurant",'
                         '"date_joined":"2025-10-26T14:00:00Z"}')


def test_retrieve_non_existing(client, restaurant):
    resp = client.get(ENDPOINT + f"{restaurant.id+999}/")

    assert resp.status_code == HTTP_404_NOT_FOUND
    assert resp.text == '{"detail":"No Restaurant matches the given query."}'
