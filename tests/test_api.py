import datetime

import pytest
from fastapi.testclient import TestClient

from main import app


@pytest.fixture
def client():
    return TestClient(app)


@pytest.fixture
def token(client):
    url = "localhost:7081"
    response = client.post(
        f"{url}/auth/login", json={"username": "admin", "password": "admin"}
    )
    return response.json().get("token")


@pytest.mark.api
def test_read_root(client):
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {
        "message": "Welcome to the Processo Seletivo API - Backend Python"
    }


@pytest.mark.create_reservation
def test_create_reservation(client, token):
    url = "localhost:7081"
    reservation_data = {
        "room_id": 1,
        "start_datetime": datetime.datetime.now(),
        "end_datetime": datetime.datetime.now() + datetime.timedelta(hours=1),
        "responsible": "Test User",
        "coffee": False,
    }
    headers = {"Authorization": f"Bearer {token}"}
    response = client.post(
        f"{url}/reservations/", json=reservation_data, headers=headers
    )
    assert response.status_code == 201
    data = response.json()
    assert data["room"]["id"] == reservation_data["room_id"]
    assert data["start_datetime"] == reservation_data["start_datetime"]
    assert data["end_datetime"] == reservation_data["end_datetime"]
    assert data["responsible"] == reservation_data["responsible"]
    assert data["coffee"] == reservation_data["coffee"]
