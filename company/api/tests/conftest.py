import sys
from pathlib import Path

from django.contrib.auth import get_user_model
from django.test import Client
import pytest


sys.path.append(Path(__file__).resolve().parent)  # type:ignore


@pytest.fixture
def superuser(db):
    User = get_user_model()
    return User.objects.create_superuser(username="admin",
                                         password="password",
                                         email="admin@mail.com")


@pytest.fixture
def client():
    return Client()
