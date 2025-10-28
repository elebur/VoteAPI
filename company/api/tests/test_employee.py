from types import MappingProxyType

import pytest
from rest_framework.test import APIClient

from api.tests.tools import get_jwt_for_user, auth_client, PERMISSION_ERROR, de_json

# Using MappingProxyType to simulate "frozendict".
PAYLOAD = MappingProxyType({"first_name": "User",
                            "last_name": "Name",
                            "username": "username",
                            "password": "password",
                            "email": "user@name.com"
                            })

endpoint = "/api/employee/"


def test_employee_creation(admin, client):
    jwt = get_jwt_for_user(admin)

    client = auth_client(client, jwt)
    resp = client.post(endpoint, PAYLOAD)

    assert resp.text == '{"employee_id":1}'
    assert resp.status_code == 201


def test_creation_with_duplicate_username(admin, user, client):
    jwt = get_jwt_for_user(admin)
    client = auth_client(client, jwt)

    resp = client.post(endpoint, PAYLOAD)

    assert resp.status_code == 400
    assert resp.text == '["The username \'username\' is already in use"]'


def test_creation_by_not_admin(client, user):
    jwt = get_jwt_for_user(user)
    client = auth_client(client, jwt)
    payload = PAYLOAD.copy()
    payload["username"] = "user2"

    resp = client.post(endpoint, payload)

    assert resp.text == PERMISSION_ERROR
    assert resp.status_code == 403


def test_creation_without_username(admin, client):
    jwt = get_jwt_for_user(admin)
    payload = PAYLOAD.copy()
    payload.pop("username")

    auth_client(client, jwt)

    resp = client.post(endpoint, payload)

    assert resp.status_code == 400
    assert resp.text == '{"details":{"username":["This field is required."]}}'


def test_creation_without_password(admin, client):
    jwt = get_jwt_for_user(admin)
    payload = PAYLOAD.copy()
    payload.pop("password")

    auth_client(client, jwt)

    resp = client.post(endpoint, payload)

    assert resp.status_code == 400
    assert resp.text == '{"details":{"password":["This field is required."]}}'


def test_creation_without_first_name(admin, client):
    jwt = get_jwt_for_user(admin)
    payload = PAYLOAD.copy()
    payload.pop("first_name")

    auth_client(client, jwt)

    resp = client.post(endpoint, payload)

    assert resp.status_code == 400
    assert resp.text == '{"details":{"first_name":["This field is required."]}}'


def test_creation_without_last_name(admin, client):
    jwt = get_jwt_for_user(admin)
    payload = PAYLOAD.copy()
    payload.pop("last_name")

    auth_client(client, jwt)

    resp = client.post(endpoint, payload)

    assert resp.status_code == 400
    assert resp.text == '{"details":{"last_name":["This field is required."]}}'


def test_creation_without_email(admin, client):
    jwt = get_jwt_for_user(admin)
    payload = PAYLOAD.copy()
    payload.pop("email")

    auth_client(client, jwt)

    resp = client.post(endpoint, payload)

    assert resp.status_code == 400
    assert resp.text == '{"details":{"email":["This field is required."]}}'


def test_creation_by_anonymous_user(client):
    resp = client.post(endpoint, PAYLOAD)

    assert resp.status_code == 401
    assert resp.text == '{"detail":"Authentication credentials were not provided."}'


@pytest.mark.freeze_time("2025-10-26T14:00:00")
def test_retrieving_employee_by_admin(admin, employee, client):
    jwt = get_jwt_for_user(admin)
    client = auth_client(client, jwt)
    resp = client.get(endpoint + f"{employee.id}/")

    resp_json = de_json(resp.text)

    assert resp_json == {"id": 1,
                         "first_name": "John",
                         "last_name": "Doe",
                         "date_joined": "2025-10-26T14:00:00Z"}


def test_retrieving_non_existing_employee(admin, client):
    jwt = get_jwt_for_user(admin)
    client = auth_client(client, jwt)
    resp = client.get(endpoint + "9999/")


    assert resp.status_code == 404
    assert resp.text == '{"detail":"No Employee matches the given query."}'


def test_retrieving_employee_by_regular_user(user, admin, employee):
    client_user = auth_client(APIClient(), get_jwt_for_user(user))
    client_admin = auth_client(APIClient(), get_jwt_for_user(admin))

    url = endpoint + f"{employee.id}/"

    resp_user = client_user.get(url)
    resp_admin = client_admin.get(url)

    # Ensure that an admin can access the employee...
    assert resp_admin.status_code == 200
    assert "first_name" in resp_admin.text and "last_name" in resp_admin.text
    # ... and a regular user can't access the employee.
    assert resp_user.status_code == 403
    assert resp_user.text == '{"detail":"You do not have permission to perform this action."}'


def test_retrieving_employee_by_anonymous_user(client, admin, employee):
    client_admin = auth_client(APIClient(), get_jwt_for_user(admin))

    url = endpoint + f"{employee.id}/"

    anon_user = client.get(url)
    resp_admin = client_admin.get(url)

    # Ensure that an admin can access the employee...
    assert resp_admin.status_code == 200
    assert "first_name" in resp_admin.text and "last_name" in resp_admin.text
    # ... and an anonymous user can't access the employee.
    assert anon_user.status_code == 401
    assert anon_user.text == '{"detail":"Authentication credentials were not provided."}'


