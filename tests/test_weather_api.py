from unittest.mock import AsyncMock

from fastapi import HTTPException, status
from fastapi.testclient import TestClient

from app.services.weather import WeatherServiceCityNotFoundError
from app.main import app
from app.core.security import verify_api_key


async def mock_valid_api_key():
    return None


async def mock_invalid_api_key():
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Invalid or inactive API key."
    )


app.dependency_overrides[verify_api_key] = mock_valid_api_key

client = TestClient(app)


def test_get_weather_without_api_key():

    # Temporarily remove valid authentication override
    app.dependency_overrides.pop(
        verify_api_key,
        None
    )

    response = client.post(
        "/api/weather/",
        json={
            "city": "Lahore"
        }
    )

    assert response.status_code == 401

    assert response.json() == {
        "detail": "API key is required."
    }

    # Restore valid authentication
    app.dependency_overrides[verify_api_key] = (
        mock_valid_api_key
    )


def test_get_weather_wrong_api_key():

    app.dependency_overrides[verify_api_key] = (
        mock_invalid_api_key
    )

    response = client.post(
        "/api/weather/",
        headers={
            "X-API-Key": "wrong-api-key"
        },
        json={
            "city": "Lahore"
        }
    )

    assert response.status_code == 401

    assert response.json() == {
        "detail": "Invalid or inactive API key."
    }

    # Restore valid authentication
    app.dependency_overrides[verify_api_key] = (
        mock_valid_api_key
    )

def test_get_weather_invalid_city(monkeypatch):

    monkeypatch.setattr(
        "app.api.routes.weather_service.get_weather",
        AsyncMock(
            side_effect=WeatherServiceCityNotFoundError(
                "City not found."
            )
        )
    )

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


def test_get_weather_history(monkeypatch):

    mock_history = {
        "page": 1,
        "limit": 10,
        "total": 0,
        "total_pages": 0,
        "has_next": False,
        "data": []
    }

    monkeypatch.setattr(
        "app.api.routes.weather_service.get_weather_history",
        AsyncMock(return_value=mock_history)
    )

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


def test_security_headers():

    response = client.get("/")

    assert response.status_code == 200

    assert (
        response.headers["X-Content-Type-Options"]
        == "nosniff"
    )

    assert (
        response.headers["X-Frame-Options"]
        == "DENY"
    )

    assert (
        response.headers["Referrer-Policy"]
        == "strict-origin-when-cross-origin"
    )

    assert "Permissions-Policy" in response.headers