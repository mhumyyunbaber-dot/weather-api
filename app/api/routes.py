from fastapi import APIRouter, HTTPException, Query

from app.schemas import WeatherRequest, WeatherResponse
from app.services.weather import (
    WeatherService,
    WeatherServiceAPIError,
    WeatherServiceConnectionError,
    WeatherServiceTimeoutError,
    WeatherDatabaseError,
    WeatherServiceCityNotFoundError
)


router = APIRouter(
    prefix="/weather",
    tags=["Weather"]
)


weather_service = WeatherService()


@router.post(
    "/",
    response_model=WeatherResponse
)
async def get_weather(request: WeatherRequest):

    try:

        weather = await weather_service.get_weather(
            request.city
        )

        return weather

    except WeatherServiceCityNotFoundError:

        raise HTTPException(
            status_code=404,
            detail="City not found."
        )

    except WeatherServiceTimeoutError:

        raise HTTPException(
            status_code=504,
            detail="Weather service request timed out."
        )

    except WeatherServiceConnectionError:

        raise HTTPException(
            status_code=502,
            detail="Unable to connect to weather service."
        )

    except WeatherServiceAPIError:

        raise HTTPException(
            status_code=502,
            detail="Weather service returned an error."
        )

    except WeatherDatabaseError:

        raise HTTPException(
            status_code=500,
            detail="Unable to save weather data."
        )

    except Exception:

        raise HTTPException(
            status_code=500,
            detail="Internal server error."
        )


@router.get("/history")
async def get_weather_history(
    city: str | None = None,
    page: int = Query(default=1, ge=1),
    limit: int = Query(default=10, ge=1, le=100)
):

    try:

        history = await weather_service.get_weather_history(
            city=city,
            page=page,
            limit=limit
        )

        return history

    except WeatherDatabaseError:

        raise HTTPException(
            status_code=500,
            detail="Unable to fetch weather history."
        )

    except Exception:

        raise HTTPException(
            status_code=500,
            detail="Internal server error."
        )