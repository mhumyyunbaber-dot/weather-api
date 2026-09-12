import time

from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware

from app.services.usage import UsageService


class UsageTrackingMiddleware(BaseHTTPMiddleware):

    async def dispatch(
        self,
        request: Request,
        call_next
    ):

        start_time = time.perf_counter()

        response = await call_next(request)

        response_time_ms = (
            time.perf_counter() - start_time
        ) * 1000

        developer_name = getattr(
            request.state,
            "developer_name",
            None
        )

        api_key_hash = getattr(
            request.state,
            "api_key_hash",
            None
        )

        # Track only authenticated developer requests
        if developer_name and api_key_hash:

            usage_service = UsageService()

            try:

                await usage_service.track_usage(
                    developer_name=developer_name,
                    api_key_hash=api_key_hash,
                    endpoint=request.url.path,
                    method=request.method,
                    status_code=response.status_code,
                    response_time_ms=round(
                        response_time_ms,
                        2
                    )
                )

            except Exception:
                # Usage tracking must never break the API
                pass

        return response