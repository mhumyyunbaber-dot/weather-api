from datetime import datetime, timezone
import hashlib
import secrets


def generate_api_key() -> str:
    """
    Generate a secure API key for a developer.
    """
    return f"wapi_{secrets.token_urlsafe(32)}"


def hash_api_key(api_key: str) -> str:
    """
    Create a SHA-256 hash of an API key.
    """
    return hashlib.sha256(
        api_key.encode("utf-8")
    ).hexdigest()


def create_api_key_document(
    developer_name: str,
    api_key: str
) -> dict:
    """
    Create the MongoDB document for an API key.
    """

    return {
        "developer_name": developer_name,
        "key_hash": hash_api_key(api_key),
        "is_active": True,
        "created_at": datetime.now(timezone.utc)
    }