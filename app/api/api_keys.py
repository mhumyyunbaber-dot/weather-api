from fastapi import APIRouter, Depends, HTTPException, status, Request

from app.core.limiter import limiter
from app.core.admin_security import verify_admin_api_key

from app.schemas import (
    APIKeyCreateRequest,
    APIKeyCreateResponse,
    APIKeyRevokeRequest
)

from app.services.api_keys import APIKeyService


router = APIRouter(
    prefix="/keys",
    tags=["API Keys"]
)


api_key_service = APIKeyService()

@router.post(
    "/create",
    response_model=APIKeyCreateResponse,
    status_code=status.HTTP_201_CREATED
)
@limiter.limit("5/minute")
async def create_api_key(
    request: Request,
    api_key_request: APIKeyCreateRequest,
    _: None = Depends(verify_admin_api_key)
):

    api_key = await api_key_service.create_api_key(
        api_key_request.developer_name
    )

    return {
        "developer_name": api_key_request.developer_name,
        "api_key": api_key,
        "message": (
            "API key created successfully. "
            "Store it securely because it cannot be retrieved again."
        )
    }


@router.post(
    "/revoke",
    status_code=status.HTTP_200_OK
)
@limiter.limit("10/minute")
async def revoke_api_key(
    request: Request,
    api_key_request: APIKeyRevokeRequest,
    _: None = Depends(verify_admin_api_key)
):

    revoked = await api_key_service.revoke_api_key(
        api_key_request.api_key
    )

    if not revoked:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="API key not found or already inactive."
        )

    return {
        "message": "API key revoked successfully."
    }