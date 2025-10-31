from copy import deepcopy

import pytest
from rest_framework.status import (
    HTTP_200_OK,
    HTTP_201_CREATED,
    HTTP_400_BAD_REQUEST,
    HTTP_401_UNAUTHORIZED,
    HTTP_404_NOT_FOUND,
)

from api.tests.tools import AUTH_REQUIRED_401, auth_client, de_json, get_jwt_for_user

MENU_ITEMS = (
    {
        "title": "Bruschetta al Pomodoro",
        "description": "Toasted bread topped with fresh tomatoes, basil, and olive oil",
    },
    {
        "title": "Risotto ai Funghi Porcini",
        "description": "Creamy risotto with porcini mushrooms and Parmesan cheese",
    },
    {
        "title": "Spaghetti Carbonara",
        "description": "Classic pasta with egg, pancetta, and Pecorino Romano cheese.",
    },
    {
        "title": "Lasagna alla Bolognese",
        "description": "Layered pasta with Bolognese meat sauce and béchamel cream.",
    },
    {
        "title": "Tiramisu",
        "description": "Traditional Italian dessert made with mascarpone, coffee.",
    },
)

MENU_REQUEST_BODY = {
    "restaurant": 1,
    "title": "Italian",
    "notes": "Monday's menu",
    "launch_date": "2025-10-26",
    "items": MENU_ITEMS,
}

MULTIPLE_MENUS_STRUCTURE = [
    {
        "id": 1,
        "items": [
            {"id": 1, "title": "Item#1_1", "description": "Descr#1_1"},
            {"id": 2, "title": "Item#1_2", "description": "Descr#1_2"},
        ],
        "title": "",
        "notes": "",
        "launch_date": "2025-10-16",
        "date_created": "2025-10-16T19:00:00Z",
        "last_modified": "2025-10-16T19:00:00Z",
        "restaurant": 1,
    },
    {
        "id": 3,
        "items": [
            {"id": 4, "title": "Item#2_1", "description": "Descr#3_1"},
            {"id": 5, "title": "Item#3_2", "description": "Descr#3_2"},
        ],
        "title": "",
        "notes": "",
        "launch_date": "2025-10-16",
        "date_created": "2025-10-16T19:00:00Z",
        "last_modified": "2025-10-16T19:00:00Z",
        "restaurant": 3,
    },
    {
        "id": 4,
        "items": [
            {"id": 6, "title": "Item#4_1", "description": "Descr#4_1"},
            {"id": 7, "title": "Item#4_2", "description": "Descr#4_2"},
            {"id": 8, "title": "Item#4_3", "description": "Descr#4_3"},
        ],
        "title": "",
        "notes": "",
        "launch_date": "2025-10-16",
        "date_created": "2025-10-16T19:00:00Z",
        "last_modified": "2025-10-16T19:00:00Z",
        "restaurant": 4,
    },
]

ENDPOINT = "/api/menu/"


def test_create_by_admin(admin, client, restaurant):
    client = auth_client(client, get_jwt_for_user(admin))

    resp = client.post(ENDPOINT, MENU_REQUEST_BODY)

    assert resp.status_code == HTTP_201_CREATED
    assert resp.text == '{"menu_id":1}'


def test_create_by_user(user, client, restaurant):
    client = auth_client(client, get_jwt_for_user(user))

    resp = client.post(ENDPOINT, MENU_REQUEST_BODY)

    assert resp.text == '{"menu_id":1}'
    assert resp.status_code == HTTP_201_CREATED


def test_create_by_anonymous(client, restaurant):

    resp = client.post(ENDPOINT, MENU_REQUEST_BODY)

    assert resp.text == AUTH_REQUIRED_401
    assert resp.status_code == HTTP_401_UNAUTHORIZED


def test_create_without_items(user, client, restaurant):
    client = auth_client(client, get_jwt_for_user(user))

    payload = deepcopy(MENU_REQUEST_BODY)
    payload["items"] = []

    resp = client.post(ENDPOINT, payload)

    assert resp.text == ("""{"details":"'items' is the required parameter. """
                         """It can\'t be null or an empty array"}""")
    assert resp.status_code == HTTP_400_BAD_REQUEST


def test_create_with_item_without_title(client, user, restaurant):
    client = auth_client(client, get_jwt_for_user(user))

    payload = deepcopy(MENU_REQUEST_BODY)
    payload["items"][0].pop("title")

    resp = client.post(ENDPOINT, payload)

    assert resp.text == ('{"details":{"items":[{"title":'
                         '["This field is required."]},{},{},{},{}]}}')
    assert resp.status_code == HTTP_400_BAD_REQUEST


def test_create_with_item_without_description(client, user, restaurant):
    client = auth_client(client, get_jwt_for_user(user))

    payload = deepcopy(MENU_REQUEST_BODY)
    payload["items"][0].pop("description")

    resp = client.post(ENDPOINT, payload)

    assert resp.text == ('{"details":{"items":[{"description":'
                         '["This field is required."]},{},{},{},{}]}}')
    assert resp.status_code == HTTP_400_BAD_REQUEST


def test_admin_creates_menu_without_restaurant(admin, client, restaurant):
    client = auth_client(client, get_jwt_for_user(admin))

    payload = deepcopy(MENU_REQUEST_BODY)
    payload.pop("restaurant")
    resp = client.post(ENDPOINT, payload)

    assert resp.text == '{"details":{"restaurant":["This field is required."]}}'
    assert resp.status_code == HTTP_400_BAD_REQUEST


def test_admin_creates_menu_with_non_existing_restaurant(admin, client, restaurant):
    client = auth_client(client, get_jwt_for_user(admin))

    payload = deepcopy(MENU_REQUEST_BODY)
    payload["restaurant"] = 9999
    resp = client.post(ENDPOINT, payload)

    assert resp.text == ('{"details":{"restaurant":'
                         '["Invalid pk \\"9999\\" - object does not exist."]}}')
    assert resp.status_code == HTTP_400_BAD_REQUEST


def test_create_without_title(client, user, restaurant):
    client = auth_client(client, get_jwt_for_user(user))
    payload = deepcopy(MENU_REQUEST_BODY)
    payload.pop("title")

    resp = client.post(ENDPOINT, payload)

    assert resp.text == '{"menu_id":1}'
    assert resp.status_code == HTTP_201_CREATED


def test_create_without_notes(client, user, restaurant):
    client = auth_client(client, get_jwt_for_user(user))
    payload = deepcopy(MENU_REQUEST_BODY)
    payload.pop("notes")

    resp = client.post(ENDPOINT, payload)

    assert resp.text == '{"menu_id":1}'
    assert resp.status_code == HTTP_201_CREATED


def test_create_without_launch_date(client, user, restaurant):
    client = auth_client(client, get_jwt_for_user(user))
    payload = deepcopy(MENU_REQUEST_BODY)
    payload.pop("launch_date")

    resp = client.post(ENDPOINT, payload)

    assert resp.text == '{"details":{"launch_date":["This field is required."]}}'
    assert resp.status_code == HTTP_400_BAD_REQUEST


@pytest.mark.freeze_time("2025-10-16T11:00:00Z")
def test_retrieve_by_id_by_user(client, user, restaurant, menu):
    client = auth_client(client, get_jwt_for_user(user))
    resp = client.get(ENDPOINT + f"{menu.id}/")

    assert resp.text == ('{"id":1,"items":['
                         '{"id":1,"title":"Menu item","description":"Description"}],'
                         '"title":"","notes":"","launch_date":"2025-10-16",'
                         '"date_created":"2025-10-16T11:00:00Z",'
                         '"last_modified":"2025-10-16T11:00:00Z","restaurant":2}')
    assert resp.status_code == HTTP_200_OK


@pytest.mark.freeze_time("2025-10-16T11:00:00Z")
def test_retrieve_by_id_by_admin(client, admin, restaurant, menu):
    client = auth_client(client, get_jwt_for_user(admin))
    resp = client.get(ENDPOINT + f"{menu.id}/")

    assert resp.text == ('{"id":1,"items":['
                         '{"id":1,"title":"Menu item","description":"Description"}],'
                         '"title":"","notes":"","launch_date":"2025-10-16",'
                         '"date_created":"2025-10-16T11:00:00Z",'
                         '"last_modified":"2025-10-16T11:00:00Z","restaurant":2}')
    assert resp.status_code == HTTP_200_OK


@pytest.mark.freeze_time("2025-10-16T11:00:00Z")
def test_retrieve_by_id_by_anonymous(client, restaurant, menu):
    resp = client.get(ENDPOINT + f"{menu.id}/")

    assert resp.text == ('{"id":1,"items":['
                         '{"id":1,"title":"Menu item","description":"Description"}],'
                         '"title":"","notes":"","launch_date":"2025-10-16",'
                         '"date_created":"2025-10-16T11:00:00Z",'
                         '"last_modified":"2025-10-16T11:00:00Z","restaurant":2}')
    assert resp.status_code == HTTP_200_OK


def test_retrieve_non_existing(client, admin, restaurant, menu):
    client = auth_client(client, get_jwt_for_user(admin))
    resp = client.get(ENDPOINT + f"{menu.id+1000}/")

    assert resp.text == '{"detail":"No Menu matches the given query."}'
    assert resp.status_code == HTTP_404_NOT_FOUND


@pytest.mark.freeze_time("2025-10-16T19:00:00Z")
def test_retrieve_without_id(client, admin, multiple_menus):
    client = auth_client(client, get_jwt_for_user(admin))
    resp = client.get(ENDPOINT)

    assert de_json(resp.text) == MULTIPLE_MENUS_STRUCTURE
    assert resp.status_code == HTTP_200_OK


@pytest.mark.freeze_time("2025-10-16T19:00:00Z")
def test_with_today_date(client, multiple_menus):
    resp = client.get(ENDPOINT + "2025-10-16/")

    assert de_json(resp.text) == MULTIPLE_MENUS_STRUCTURE
    assert resp.status_code == HTTP_200_OK

@pytest.mark.freeze_time("2025-10-16T19:00:00Z")
def test_with_date_in_future(client, multiple_menus):
    resp = client.get(ENDPOINT + "2026-10-16/")  # 1 year in the future.

    assert resp.status_code == HTTP_200_OK
    assert resp.text == "[]"


def test_with_bad_date(client, multiple_menus):
    resp = client.get(ENDPOINT + "9999-99-99/")

    assert resp.status_code == HTTP_400_BAD_REQUEST
    assert resp.text == ('{"details":"Invalid date - \'9999-99-99\'. '
                         'Correct format is YYYY-MM-DD"}')
