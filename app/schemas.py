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