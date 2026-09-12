from fastapi import Header, HTTPException, Request, status

from app.services.api_keys import APIKeyService


api_key_service = APIKeyService()


async def verify_api_key(
    request: Request,
    x_api_key: str | None = Header(default=None)
) -> None:

    if not x_api_key:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="API key is required."
        )

    document = await api_key_service.verify_api_key(
        x_api_key
    )

    if not document:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or inactive API key."
        )

    request.state.developer_name = document["developer_name"]

    request.state.api_key_hash = document["key_hash"]