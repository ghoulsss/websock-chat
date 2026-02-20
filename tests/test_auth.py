import pytest
from fastapi.testclient import TestClient

from src.core.config import settings
from main import app
from jose import jwt

SECRET_KEY = settings().SECRET_KEY
ALGORITHM = settings().ALGORITHM

client = TestClient(app)


def test_success_login():
    response = client.post("/auth/login", params={
        "email": "dan@mail.ru",
        "password": "admin"
    })
    assert response.status_code == 200
    assert "access_token" in response.json()


def test_invalid_login():
    response = client.post("/auth/login", params={
        "email": "admin",
        "password": "wrong"
    })
    assert response.status_code == 401


def test_access_protected_with_token():
    login = client.post("/auth/login", params={
        "email": "dan@mail.ru",
        "password": "admin"
    })
    token = login.json()["access_token"]

    response = client.get(
        "/protected",
        headers={"Authorization": f"Bearer {token}"}
    )

    assert response.status_code == 200
    assert response.json()["message"] == "Hello admin"


def test_access_without_token():
    response = client.get("/protected")
    assert response.status_code == 401


def test_access_with_invalid_token():
    response = client.get(
        "/protected",
        headers={"Authorization": "Bearer invalidtoken"}
    )
    assert response.status_code == 401