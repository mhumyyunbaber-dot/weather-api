import hashlib

from fastapi import Request
from slowapi import Limiter


def get_api_key_identifier(request: Request) -> str:

    api_key = request.headers.get("X-API-Key")

    if api_key:

        return hashlib.sha256(
            api_key.encode()
        ).hexdigest()

    return request.client.host


limiter = Limiter(
    key_func=get_api_key_identifier
)