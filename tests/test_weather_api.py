import pytest
from fastapi.testclient import TestClient
from unittest.mock import AsyncMock

from app.main import app


client = TestClient(app)


def test_get_weather_invalid_city():

    response = client.post(
        "/api/weather/",
        json={
            "city": "ll"
        }
    )

    assert response.status_code == 404

    assert response.json() == {
        "detail": "City not found."
    }


def test_get_weather_invalid_request():

    response = client.post(
        "/api/weather/",
        json={
            "city": ""
        }
    )

    assert response.status_code == 422


def test_get_weather_missing_city():

    response = client.post(
        "/api/weather/",
        json={}
    )

    assert response.status_code == 422


def test_get_weather_history():

    response = client.get(
        "/api/weather/history"
    )

    assert response.status_code == 200

    data = response.json()

    assert "page" in data
    assert "limit" in data
    assert "total" in data
    assert "total_pages" in data
    assert "has_next" in data
    assert "data" in data
    
    from unittest.mock import AsyncMock


def test_get_weather_success(monkeypatch):

    mock_weather = {
        "city": "Lahore",
        "temperature": 30.5,
        "humidity": 50,
        "description": "clear sky",
        "searched_at": "2026-09-05T12:00:00"
    }

    monkeypatch.setattr(
        "app.api.routes.weather_service.get_weather",
        AsyncMock(return_value=mock_weather)
    )

    response = client.post(
        "/api/weather/",
        json={
            "city": "Lahore"
        }
    )

    assert response.status_code == 200

    data = response.json()

    assert data["city"] == "Lahore"
    assert data["temperature"] == 30.5
    assert data["humidity"] == 50
    assert data["description"] == "clear sky"