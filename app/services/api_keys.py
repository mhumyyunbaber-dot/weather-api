from app.database import api_keys_collection
from app.models.api_key import (
    create_api_key_document,
    generate_api_key,
    hash_api_key
)


class APIKeyService:

    async def create_api_key(
        self,
        developer_name: str
    ) -> str:

        api_key = generate_api_key()

        document = create_api_key_document(
            developer_name=developer_name,
            api_key=api_key
        )

        await api_keys_collection.insert_one(
            document
        )

        return api_key


    async def verify_api_key(
        self,
        api_key: str
    ) -> dict | None:

        key_hash = hash_api_key(api_key)

        document = await api_keys_collection.find_one(
        {
            "key_hash": key_hash,
            "is_active": True
        }
    )

        return document

    async def revoke_api_key(
        self,
        api_key: str
    ) -> bool:

        key_hash = hash_api_key(api_key)

        result = await api_keys_collection.update_one(
            {
                "key_hash": key_hash
            },
            {
                "$set": {
                    "is_active": False
                }
            }
        )

        return result.modified_count > 0