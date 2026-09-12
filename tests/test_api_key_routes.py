from unittest.mock import AsyncMock

from fastapi import HTTPException, status
from fastapi.testclient import TestClient

from app.main import app
from app.core.admin_security import verify_admin_api_key


async def mock_valid_admin():
    return None


async def mock_invalid_admin():
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Invalid admin API key."
    )


app.dependency_overrides[
    verify_admin_api_key
] = mock_valid_admin


client = TestClient(app)


def test_create_api_key_without_admin_key():

    app.dependency_overrides.pop(
        verify_admin_api_key,
        None
    )

    response = client.post(
        "/api/keys/create",
        json={
            "developer_name": "Test Developer"
        }
    )

    assert response.status_code == 401

    assert response.json() == {
        "detail": "Admin API key is required."
    }

    app.dependency_overrides[
        verify_admin_api_key
    ] = mock_valid_admin


def test_create_api_key_wrong_admin_key():

    app.dependency_overrides[
        verify_admin_api_key
    ] = mock_invalid_admin

    response = client.post(
        "/api/keys/create",
        headers={
            "X-Admin-API-Key": "wrong-key"
        },
        json={
            "developer_name": "Test Developer"
        }
    )

    assert response.status_code == 401

    assert response.json() == {
        "detail": "Invalid admin API key."
    }

    app.dependency_overrides[
        verify_admin_api_key
    ] = mock_valid_admin


def test_create_api_key_success(monkeypatch):

    mock_api_key = "wapi_test_generated_key_123456"

    monkeypatch.setattr(
        "app.api.api_keys.api_key_service.create_api_key",
        AsyncMock(return_value=mock_api_key)
    )

    response = client.post(
        "/api/keys/create",
        json={
            "developer_name": "Test Developer"
        }
    )

    assert response.status_code == 201

    data = response.json()

    assert data["developer_name"] == "Test Developer"
    assert data["api_key"] == mock_api_key
    assert "message" in data
    
def test_revoke_api_key_success(monkeypatch):

    monkeypatch.setattr(
        "app.api.api_keys.api_key_service.revoke_api_key",
        AsyncMock(return_value=True)
    )

    response = client.post(
        "/api/keys/revoke",
        json={
            "api_key": "wapi_test_key_123456789"
        }
    )

    assert response.status_code == 200

    assert response.json() == {
        "message": "API key revoked successfully."
    }


def test_revoke_api_key_not_found(monkeypatch):

    monkeypatch.setattr(
        "app.api.api_keys.api_key_service.revoke_api_key",
        AsyncMock(return_value=False)
    )

    response = client.post(
        "/api/keys/revoke",
        json={
            "api_key": "wapi_unknown_key_123456789"
        }
    )

    assert response.status_code == 404

    assert response.json() == {
        "detail": "API key not found or already inactive."
    }


def test_revoke_api_key_without_admin_key():

    app.dependency_overrides.pop(
        verify_admin_api_key,
        None
    )

    response = client.post(
        "/api/keys/revoke",
        json={
            "api_key": "wapi_test_key_123456789"
        }
    )

    assert response.status_code == 401

    assert response.json() == {
        "detail": "Admin API key is required."
    }

    app.dependency_overrides[
        verify_admin_api_key
    ] = mock_valid_admin