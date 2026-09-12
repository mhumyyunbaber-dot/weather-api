from fastapi import APIRouter, Depends, HTTPException, Query, Request

from app.core.security import verify_api_key
from app.core.limiter import limiter
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
@limiter.limit("10/minute")
async def get_weather(
    request: Request,
    weather_request: WeatherRequest,
    _: None = Depends(verify_api_key)
):

    try:

        weather = await weather_service.get_weather(
            weather_request.city
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
@limiter.limit("30/minute")
async def get_weather_history(
    request: Request,
    city: str | None = Query(
        default=None,
        min_length=2,
        max_length=100
    ),
    page: int = Query(default=1, ge=1, le=10000),
    limit: int = Query(default=10, ge=1, le=100),
    _: None = Depends(verify_api_key)
):
    try:

        if city:
            city = city.strip()

            if not city:
                raise HTTPException(
                    status_code=422,
                    detail="City name cannot be empty."
                )

            if "\x00" in city:
                raise HTTPException(
                    status_code=422,
                    detail="City name contains invalid characters."
                )

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

    except HTTPException:
        raise

    except Exception:

        raise HTTPException(
            status_code=500,
            detail="Internal server error."
        )