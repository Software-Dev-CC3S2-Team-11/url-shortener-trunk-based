import pytest
from app import app
from fastapi.testclient import TestClient
from unittest.mock import MagicMock
from database.db import get_db
from services.auth import bcrypt_context
from models.User import User
from services import auth



@pytest.fixture(autouse=True)
def clear_overrides():
    app.dependency_overrides = {}


@pytest.fixture
def client():
    return TestClient(app)


@pytest.fixture
def mock_db():
    return MagicMock()


@pytest.fixture
def override_db(mock_db):
    app.dependency_overrides[get_db] = lambda: mock_db
    return mock_db


@pytest.fixture
def valid_user():
    plain_password = "12345"
    return User(
        email="tester@tester.com",
        username="tester",
        password=bcrypt_context.hash(plain_password)
    )


@pytest.fixture
def user_data():
    return {
        "email": "testuser@example.com",
        "username": "testuser"
    }


@pytest.fixture
def secret_key():
    return auth.SECRET_KEY


@pytest.fixture
def algorithm():
    return auth.ALGORITHM
