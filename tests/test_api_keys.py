import pytest
from unittest.mock import AsyncMock

from app.models.api_key import (
    generate_api_key,
    hash_api_key,
    create_api_key_document
)
from app.services.api_keys import APIKeyService


def test_generate_api_key():

    api_key = generate_api_key()

    assert api_key.startswith("wapi_")
    assert len(api_key) > 30


def test_hash_api_key():

    api_key = "wapi_test_key"

    hashed_key = hash_api_key(api_key)

    assert hashed_key != api_key
    assert len(hashed_key) == 64


def test_create_api_key_document():

    api_key = "wapi_test_key"

    document = create_api_key_document(
        developer_name="Test Developer",
        api_key=api_key
    )

    assert document["developer_name"] == "Test Developer"
    assert document["is_active"] is True
    assert document["key_hash"] == hash_api_key(api_key)
    assert "created_at" in document


@pytest.mark.asyncio
async def test_verify_valid_api_key(monkeypatch):

    api_key = "wapi_valid_test_key"

    mock_collection = AsyncMock()

    mock_collection.find_one.return_value = {
        "developer_name": "Test Developer",
        "key_hash": hash_api_key(api_key),
        "is_active": True
    }

    monkeypatch.setattr(
        "app.services.api_keys.api_keys_collection",
        mock_collection
    )

    service = APIKeyService()

    result = await service.verify_api_key(api_key)

    assert result is not None
    assert result["developer_name"] == "Test Developer"
    assert result["key_hash"] == hash_api_key(api_key)
    assert result["is_active"] is True
    
    
@pytest.mark.asyncio
async def test_verify_invalid_api_key(monkeypatch):

    mock_collection = AsyncMock()

    mock_collection.find_one.return_value = None

    monkeypatch.setattr(
        "app.services.api_keys.api_keys_collection",
        mock_collection
    )

    service = APIKeyService()

    result = await service.verify_api_key(
        "wapi_invalid_key"
    )

    assert result is None