from datetime import datetime

from pydantic import BaseModel, Field, field_validator


class WeatherRequest(BaseModel):

    city: str = Field(
        min_length=2,
        max_length=100,
        description="Name of the city"
    )

    @field_validator("city")
    @classmethod
    def validate_city(cls, value: str) -> str:

        value = value.strip()

        if not value:
            raise ValueError("City name cannot be empty.")

        if "\x00" in value:
            raise ValueError("City name contains invalid characters.")

        return value


class WeatherResponse(BaseModel):

    city: str

    temperature: float

    humidity: int = Field(
        ge=0,
        le=100
    )

    description: str

    searched_at: datetime
    
class APIKeyCreateRequest(BaseModel):

    developer_name: str = Field(
        min_length=2,
        max_length=100,
        description="Name of the developer"
    )

    @field_validator("developer_name")
    @classmethod
    def validate_developer_name(
        cls,
        value: str
    ) -> str:

        value = value.strip()

        if not value:
            raise ValueError(
                "Developer name cannot be empty."
            )

        if "\x00" in value:
            raise ValueError(
                "Developer name contains invalid characters."
            )

        return value


class APIKeyCreateResponse(BaseModel):

    developer_name: str

    api_key: str

    message: str


class APIKeyRevokeRequest(BaseModel):

    api_key: str = Field(
        min_length=10,
        max_length=200,
        description="Developer API key to revoke"
    )

    @field_validator("api_key")
    @classmethod
    def validate_api_key(
        cls,
        value: str
    ) -> str:

        value = value.strip()

        if not value:
            raise ValueError(
                "API key cannot be empty."
            )

        if "\x00" in value:
            raise ValueError(
                "API key contains invalid characters."
            )

        return value