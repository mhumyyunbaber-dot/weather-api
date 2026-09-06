import httpx
import logging

from app.config import settings
from app.database import weather_collection
from app.models.weather import create_weather_document


class WeatherServiceError(Exception):
    pass


class WeatherServiceTimeoutError(WeatherServiceError):
    pass


class WeatherServiceConnectionError(WeatherServiceError):
    pass


class WeatherServiceAPIError(WeatherServiceError):
    pass

class WeatherServiceCityNotFoundError(WeatherServiceError):
    pass

class WeatherDatabaseError(WeatherServiceError):
    pass


class WeatherService:
    logger = logging.getLogger(__name__)

    async def get_weather(self, city: str) -> dict:

        params = {
            "q": city,
            "appid": settings.weather_api_key,
            "units": "metric"
        }

        self.logger.info(
            "Fetching weather data for city: %s",
            city
        )

        try:
            async with httpx.AsyncClient(timeout=10.0) as client:

                response = await client.get(
                    settings.weather_api_url,
                    params=params
                )

                response.raise_for_status()

                data = response.json()

                self.logger.info(
                    "Weather data fetched successfully for city: %s",
                    city
                )

        except httpx.TimeoutException:

            self.logger.error(
                "Weather service request timed out for city: %s",
                city
            )

            raise WeatherServiceTimeoutError(
                "Weather service request timed out."
            )

        except httpx.HTTPStatusError as e:

            if e.response.status_code == 404:

                self.logger.warning(
                "City not found: %s",
                city
                )

                raise WeatherServiceCityNotFoundError(
                "City not found."
                )

            self.logger.error(
                "Weather service returned an HTTP error for city: %s",
                city
            )

            raise WeatherServiceAPIError(
                "Weather service returned an error."
            )
            
        

        except httpx.RequestError:

            self.logger.error(
                "Unable to connect to weather service for city: %s",
                city
            )

            raise WeatherServiceConnectionError(
                "Unable to connect to weather service."
            )

        weather = create_weather_document(
            city=data["name"],
            temperature=data["main"]["temp"],
            humidity=data["main"]["humidity"],
            description=data["weather"][0]["description"]
        )

        # Save weather data to MongoDB
        try:

            await weather_collection.insert_one(weather)

        except Exception as e:

            self.logger.exception(
                "Failed to save weather data to database for city: %s",
                city
            )

            raise WeatherDatabaseError(
                "Failed to save weather data."
            ) from e

        self.logger.info(
            "Weather data saved to database for city: %s",
            city
        )

        return weather

    async def get_weather_history(
        self,
        city: str | None = None,
        page: int = 1,
        limit: int = 10
    ) -> dict:

        query = {}

        if city:
            query["city"] = city

        try:

            total = await weather_collection.count_documents(query)

            skip = (page - 1) * limit

            cursor = (
                weather_collection.find(query)
                .sort("searched_at", -1)
                .skip(skip)
                .limit(limit)
            )

            history = await cursor.to_list(length=limit)

        except Exception as e:

            self.logger.exception(
                "Failed to fetch weather history from database."
            )

            raise WeatherDatabaseError(
                "Failed to fetch weather history."
            ) from e

        for item in history:
            item["_id"] = str(item["_id"])

        total_pages = (total + limit - 1) // limit

        return {
            "page": page,
            "limit": limit,
            "total": total,
            "total_pages": total_pages,
            "has_next": page < total_pages,
            "data": history
        }