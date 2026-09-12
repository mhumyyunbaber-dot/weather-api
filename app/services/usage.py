from app.database import usage_collection
from app.models.usage import create_usage_document


class UsageService:

    async def track_usage(
        self,
        developer_name: str,
        api_key_hash: str,
        endpoint: str,
        method: str,
        status_code: int,
        response_time_ms: float
    ) -> None:

        document = create_usage_document(
            developer_name=developer_name,
            api_key_hash=api_key_hash,
            endpoint=endpoint,
            method=method,
            status_code=status_code,
            response_time_ms=response_time_ms
        )

        await usage_collection.insert_one(
            document
        )