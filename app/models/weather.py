from datetime import datetime, timezone


def create_weather_document(
    city: str,
    temperature: float,
    humidity: int,
    description: str
) -> dict:
    """
    Create a weather document for MongoDB.
    """

    return {
        "city": city,
        "temperature": temperature,
        "humidity": humidity,
        "description": description,
        "searched_at": datetime.now(timezone.utc)
    }