# ruff: noqa: S106
import sys
from datetime import timedelta
from pathlib import Path

import pytest
from django.contrib.auth.models import User
from django.utils import timezone
from rest_framework.response import Response
from rest_framework.test import APIClient

from base.models import Employee, Menu, Restaurant

sys.path.append(str(Path(__file__).resolve().parent))

class _JsonAPIClient(APIClient):
    """
    A simple wrapper to get rid of typing 'format="json"' in each
    POST request.
    """
    def post(self, path, data=None, format="json", content_type=None,  # noqa: A002
             follow=False, **extra) -> Response:  # noqa: ANN003, FBT002
        return super().post(
            path,
            data=data,
            format=format,
            content_type=content_type,
            follow=follow,
            **extra,
        )  # pyright: ignore[reportReturnType]


@pytest.fixture
def admin(db):
    return User.objects.create_superuser(
        username="admin", password="password", email="admin@mail.com",
    )


@pytest.fixture
def user(db):
    return User.objects.create(
        username="username", password="password", email="user@name.com",
    )


@pytest.fixture
def employee(db):
    user = User.objects.create(
        username="employee", password="password", email="user@name.com",
    )
    return Employee.objects.create(first_name="John", last_name="Doe", user=user)


@pytest.fixture
def restaurant(db):
    user = User.objects.create(
        username="restaurant_user", password="password", email="restaurant@name.com",
    )
    return Restaurant.objects.create(name="Restaurant", user=user)


@pytest.fixture
def menu(db):
    r_user = User.objects.create(
        username="menu_restaurant_user", password="password", email="restaurant@name.com",
    )
    restaurant = Restaurant.objects.create(
        name="Restaurant For Menu Fixture", user=r_user,
    )
    menu: Menu = Menu.objects.create(
        restaurant=restaurant, launch_date=timezone.now().date(),
    )
    menu.items.create(
        restaurant=restaurant, title="Menu item", description="Description",
    )

    return menu


@pytest.fixture
def multiple_menus(db):
    u1 = User.objects.create(username="rest1", password="pass")
    r1 = Restaurant.objects.create(name="Restaurant#1", user=u1)

    u2 = User.objects.create(username="rest2", password="pass")
    r2 = Restaurant.objects.create(name="Restaurant#2", user=u2)

    u3 = User.objects.create(username="rest3", password="pass")
    r3 = Restaurant.objects.create(name="Restaurant#3", user=u3)

    u4 = User.objects.create(username="rest4", password="pass")
    r4 = Restaurant.objects.create(name="Restaurant#4", user=u4)

    today = timezone.now().date()
    menu1 = Menu.objects.create(restaurant=r1, launch_date=today)
    menu2 = Menu.objects.create(restaurant=r2, launch_date=today - timedelta(days=2))
    menu3 = Menu.objects.create(restaurant=r3, launch_date=today)
    menu4 = Menu.objects.create(restaurant=r4, launch_date=today)

    menu1.items.create(restaurant=r1, title="Item#1_1", description="Descr#1_1")
    menu1.items.create(restaurant=r1, title="Item#1_2", description="Descr#1_2")

    menu2.items.create(restaurant=r2, title="Item#2_1", description="Descr#2_1")

    menu3.items.create(restaurant=r3, title="Item#2_1", description="Descr#3_1")
    menu3.items.create(restaurant=r3, title="Item#3_2", description="Descr#3_2")

    menu4.items.create(restaurant=r4, title="Item#4_1", description="Descr#4_1")
    menu4.items.create(restaurant=r4, title="Item#4_2", description="Descr#4_2")
    menu4.items.create(restaurant=r4, title="Item#4_3", description="Descr#4_3")

    return (menu1, menu2, menu3, menu4)


@pytest.fixture
def client():
    return _JsonAPIClient()
