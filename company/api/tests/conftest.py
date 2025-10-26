import sys
from pathlib import Path

from django.contrib.auth import get_user_model
from rest_framework.test import APIClient
import pytest

from base.models import Employee


sys.path.append(Path(__file__).resolve().parent)  # type:ignore


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
def client():
    return APIClient()
