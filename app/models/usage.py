from datetime import datetime, timezone


def create_usage_document(
    developer_name: str,
    api_key_hash: str,
    endpoint: str,
    method: str,
    status_code: int,
    response_time_ms: float
) -> dict:

    return {
        "developer_name": developer_name,
        "api_key_hash": api_key_hash,
        "endpoint": endpoint,
        "method": method,
        "status_code": status_code,
        "response_time_ms": response_time_ms,
        "created_at": datetime.now(timezone.utc)
    }