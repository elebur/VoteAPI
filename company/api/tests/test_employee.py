import pytest

from api.tests.tools import get_jwt_for_user, auth_client, PERMISSION_ERROR, de_json

PAYLOAD = {
    "first_name": "User",
    "last_name": "Name",
    "username": "username",
    "password": "password",
    "email": "user@name.com"
}


def test_employee_creation(admin, client):
    jwt = get_jwt_for_user(admin)

    client = auth_client(client, jwt)
    resp = client.post("/api/employee/", PAYLOAD)

    assert resp.text == '{"employee_id":1}'
    assert resp.status_code == 201


def test_creation_with_duplicate_username(admin, user, client):
    jwt = get_jwt_for_user(admin)
    client = auth_client(client, jwt)

    resp = client.post("/api/employee/", PAYLOAD)

    assert resp.status_code == 400
    assert resp.text == '["The username \'username\' is already in use"]'


def test_creation_by_not_admin(client, user):
    jwt = get_jwt_for_user(user)
    client = auth_client(client, jwt)
    PAYLOAD["username"] = "user2"

    resp = client.post("/api/employee/", PAYLOAD)

    assert resp.text == PERMISSION_ERROR
    assert resp.status_code == 403


def test_creation_without_username():
    assert 1 == 2


def test_creation_without_password():
    assert 1 == 2


def test_creation_by_anonymous_user():
    assert 1 == 2


@pytest.mark.freeze_time("2025-10-26T14:00:00")
def test_retrieving_employee_by_admin(admin, employee, client):
    jwt = get_jwt_for_user(admin)
    client = auth_client(client, jwt)
    resp = client.get("/api/employee/%s/" % employee.id)

    resp_json = de_json(resp.text)

    assert resp_json == {"id":1,
                         "first_name":"John",
                         "last_name":"Doe",
                         "date_joined":"2025-10-26T14:00:00Z"}


def test_retrieving_non_existing_employee():
    assert 1 == 2


def test_retrieving_employee_by_regular_user():
    assert 1 == 2


def test_retrieving_employee_by_anonymous_user():
    assert 1 == 2
