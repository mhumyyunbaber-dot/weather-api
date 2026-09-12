from fastapi import APIRouter, Depends

from app.core.admin_security import verify_admin_api_key
from app.services.analytics import AnalyticsService


router = APIRouter(
    prefix="/analytics",
    tags=["Analytics"]
)


analytics_service = AnalyticsService()


@router.get("/usage")
async def get_usage_summary(
    _: None = Depends(verify_admin_api_key)
):

    summary = await analytics_service.get_usage_summary()

    return summary

@router.get("/endpoints")
async def get_endpoint_usage(
    _: None = Depends(verify_admin_api_key)
):

    endpoint_usage = await analytics_service.get_endpoint_usage()

    return endpoint_usage