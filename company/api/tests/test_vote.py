import random
import string

import pytest

from base.models import User, Employee, Vote
from api.tests.tools import auth_client, de_json, get_jwt_for_user

ENDPOINT_RESULTS = "/api/vote/results/"
ENDPOINT_VOTE = "/api/menu/%s/vote/"


def generate_employees(count=1):
    def randstring(from_=4, to=10):
        return "".join(random.choices(string.ascii_letters, k=random.randint(from_, to)))

    result = list()
    for _ in range(count):
        username = randstring()
        password = randstring()
        fname = randstring()
        lname = randstring()
        email = randstring() + "example.com"
        user = User.objects.create(username=username, password=password,
                                   email=email)
        employee = Employee.objects.create(first_name=fname, last_name=lname,
                                           user=user)

        result.append(employee)

    return result


def test_retrieve_menu_without_votes(client, menu):
    resp = client.get(ENDPOINT_RESULTS)

    assert resp.text == '[{"menu_id":1,"likes":0,"dislikes":0,"result":0}]'


def test_vote(client, menu, employee):
    payload = {"employee_id": employee.id, "like": False}
    auth_client(client, get_jwt_for_user(employee.user))

    resp = client.post(ENDPOINT_VOTE % menu.id, payload)

    assert resp.text == '{"vote_id":1,"action":"disliked"}'


def test_retrieve_with_votes(client, menu):
    employees = generate_employees(5)
    for i, empl in enumerate(employees):
        like = True if i % 2 == 0 else False

        menu.votes.create(menu=menu, employee=empl, like=like)

    resp = client.get(ENDPOINT_RESULTS)

    assert resp.text == '[{"menu_id":1,"likes":3,"dislikes":2,"result":1}]'


@pytest.mark.django_db
def test_retrieve_on_the_day_without_menus(client):
    resp = client.get(ENDPOINT_RESULTS)

    assert resp.text == "[]"


def test_retrieve_results_with_multiple_menus(client, multiple_menus):
    employees = generate_employees(6)
    m1, m2, m3, m4 = multiple_menus

    # Menu #1 - all likes
    [Vote.objects.create(menu=m1, employee=e, like=True) for e in employees]

    # Menu #2 - all dislikes
    [Vote.objects.create(menu=m2, employee=e, like=False) for e in employees]

    # Menu #3 has date in the past.

    # Menu #4 - 3 likes, 3 dislikes
    for i, e in enumerate(employees):
        like = True if i%2 == 0 else False
        Vote.objects.create(menu=m4, employee=e, like=like)

    resp = client.get(ENDPOINT_RESULTS)

    assert de_json(resp.text) == [
        {"menu_id": 1, "likes": 6, "dislikes": 0, "result": 6},
        {"menu_id": 3, "likes": 0, "dislikes": 0, "result": 0},
        {"menu_id": 4, "likes": 3, "dislikes": 3, "result": 0}
    ]


def test_vote_multiple_times(client, menu, employee):
    auth_client(client, get_jwt_for_user(employee.user))

    payload = {"employee_id": employee.id, "like": True}

    resp_init = client.post(ENDPOINT_VOTE%menu.id, payload)
    resp_duplicate = client.post(ENDPOINT_VOTE%menu.id, payload)

    assert resp_init.text == '{"vote_id":1,"action":"liked"}'
    assert resp_init.status_code == 200

    assert resp_duplicate.text == '{"details":"You\'ve already liked this menu \'None\'."}'
    assert resp_duplicate.status_code == 400



def test_vote_set_like_then_dislike_for_same_menu(client, employee, menu):
    auth_client(client, get_jwt_for_user(employee.user))

    payload = {"employee_id": employee.id, "like": True}
    resp_init = client.post(ENDPOINT_VOTE%menu.id, payload)

    payload["like"] = False
    resp_duplicate = client.post(ENDPOINT_VOTE%menu.id, payload)

    assert resp_init.text == '{"vote_id":1,"action":"liked"}'
    assert resp_init.status_code == 200

    assert resp_duplicate.text == '{"details":"You\'ve already liked this menu \'None\'."}'
    assert resp_duplicate.status_code == 400


def test_vote_set_dislike_then_like_for_same_menu(client, employee, menu):
    auth_client(client, get_jwt_for_user(employee.user))

    payload = {"employee_id": employee.id, "like": False}
    resp_init = client.post(ENDPOINT_VOTE%menu.id, payload)

    payload["like"] = True
    resp_duplicate = client.post(ENDPOINT_VOTE%menu.id, payload)

    assert resp_init.text == '{"vote_id":1,"action":"disliked"}'
    assert resp_init.status_code == 200

    assert resp_duplicate.text == '{"details":"You\'ve already disliked this menu \'None\'."}'
    assert resp_duplicate.status_code == 400


def test_with_non_existing_employee(client, user, menu):
    """
    When user#1 using their JWT token, but in the
    body they send another employee ID (e.g. user#1 sends ID of the user#2)
    """
    auth_client(client, get_jwt_for_user(user))

    payload = {"like": True}
    resp = client.post(ENDPOINT_VOTE%menu.id, payload)

    assert resp.text == '{"details":"Employee not found"}'
    assert resp.status_code == 404
