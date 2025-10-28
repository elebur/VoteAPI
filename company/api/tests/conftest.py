from datetime import timedelta
import sys
from pathlib import Path

from django.contrib.auth import get_user_model
from django.utils import timezone
from rest_framework.test import APIClient
import pytest

from base.models import Employee, Restaurant, Menu


sys.path.append(Path(__file__).resolve().parent)  # type:ignore

class _JsonAPIClient(APIClient):
    """
    A simple wrapper to get rid of typing 'format="json"' in each
    POST request.
    """
    def post(self, path, data=None, format="json", content_type=None,
             follow=False, **extra):
        return super().post(path, data=data, format=format,
                            content_type=content_type, follow=follow, **extra)


@pytest.fixture
def admin(db):
    User = get_user_model()
    return User.objects.create_superuser(username="admin",
                                         password="password",
                                         email="admin@mail.com")


@pytest.fixture
def user(db):
    User = get_user_model()
    return User.objects.create(username="username",
                               password="password",
                               email="user@name.com")


@pytest.fixture
def employee(db):
    User = get_user_model()
    user = User.objects.create(username="employee",
                               password="password",
                               email="user@name.com")
    return Employee.objects.create(first_name="John",
                                   last_name="Doe",
                                   user=user)


@pytest.fixture
def restaurant(db):
    return Restaurant.objects.create(name="Restaurant")


@pytest.fixture
def menu(db):
    restaurant = Restaurant.objects.create(name="Restaurant For Menu Fixture")
    menu = Menu.objects.create(restaurant=restaurant,
                               launch_date=timezone.now().date())
    menu.items.create(restaurant=restaurant,
                      title="Menu item", description="Description")

    return menu


@pytest.fixture
def multiple_menus(db):
    r1 = Restaurant.objects.create(name="Restaurant#1")
    r2 = Restaurant.objects.create(name="Restaurant#2")
    r3 = Restaurant.objects.create(name="Restaurant#3")
    r4 = Restaurant.objects.create(name="Restaurant#4")

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

    return menu





@pytest.fixture
def client():
    return _JsonAPIClient()
