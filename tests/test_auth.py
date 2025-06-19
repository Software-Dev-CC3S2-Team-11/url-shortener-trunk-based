import pytest
from app import app
from fastapi import status
from jose import jwt
from services import auth
from datetime import datetime, timedelta


def test_register(client, override_db):
    """Test de registro de usuario"""
    response = client.post("/auth/register", data={
        "email": "newuser@test.com",
        "password": "mypassword",
        "username": "newuser"
    }, follow_redirects=False)

    assert response.status_code == status.HTTP_302_FOUND
    assert response.headers["location"] == "/"


@pytest.mark.parametrize("email, password, expected_status, expect_redirect", [
    ("tester@tester.com", "12345", 302, True),
    ("login@test.com", "wrongpassword", 200, False),
    ("nouser@test.com", "12345", 200, False),
])
def test_login(client, override_db, valid_user, email, password,
               expected_status, expect_redirect):
    """Test de inicio de sesión de usuario"""
    if email == valid_user.email:
        override_db.query.return_value.filter.return_value.first.return_value = valid_user
    else:
        override_db.query.return_value.filter.return_value.first.return_value = None

    response = client.post("/auth/login", data={
        "email": email,
        "password": password
    }, follow_redirects=False)

    assert response.status_code == expected_status
    if expect_redirect:
        assert response.headers["location"] == "/"
    else:
        assert "Invalid credentials" in response.text


def test_create_access_token(user_data, secret_key, algorithm):
    """Test de creación de token JWT"""
    token = auth.create_access_token(email=user_data["email"],
                                     username=user_data["username"])
    payload = jwt.decode(token, secret_key, algorithms=[algorithm])

    assert payload["email"] == user_data["email"]
    assert payload["username"] == user_data["username"]
    assert "exp" in payload

    expires_at = datetime.fromtimestamp(payload["exp"])
    now = datetime.utcnow()
    delta = expires_at - now
    assert timedelta(days=29) < delta <= timedelta(days=30)


@pytest.mark.parametrize("description, create_token, expected_result", [
    ("token válido",
     lambda data: auth.create_access_token(email=data["email"],
                                           username=data["username"]),
     True),

    ("token mal formado",
     lambda data: "this.is.not.jwt",
     False),

    ("token vacío",
     lambda data: "",
     False),

    ("token con firma incorrecta",
     lambda data: jwt.encode(
         {"email": data["email"], "username": data["username"],
          "exp": datetime.utcnow() + timedelta(minutes=1)},
         key="WRONG_SECRET",
         algorithm=auth.ALGORITHM
     ),
     False),
])
def test_verify_token(description, create_token, expected_result, user_data):
    """Test de verificación de token JWT"""
    generated_token = create_token(user_data)
    result = auth.verify_token(generated_token)
    if expected_result:
        assert result is not None, f"Falló: {description}"
        assert result["email"] == user_data["email"]
        assert result["username"] == user_data["username"]
    else:
        assert result is None, f"Falló: {description}"