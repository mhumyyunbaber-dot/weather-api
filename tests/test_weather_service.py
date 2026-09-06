import pytest
import httpx

from app.services.weather import (
    WeatherService,
    WeatherServiceAPIError,
    WeatherServiceCityNotFoundError,
    WeatherServiceConnectionError,
    WeatherServiceTimeoutError,
    WeatherDatabaseError,
)


class MockResponse:
    def __init__(self, status_code=200, data=None):
        self.status_code = status_code
        self._data = data or {}

    def raise_for_status(self):
        if self.status_code >= 400:
            request = httpx.Request("GET", "https://example.com")
            response = httpx.Response(self.status_code, request=request)
            raise httpx.HTTPStatusError(
                "HTTP error",
                request=request,
                response=response,
            )

    def json(self):
        return self._data


class MockAsyncClient:
    def __init__(self, response=None, exception=None, timeout=False):
        self.response = response
        self.exception = exception
        self.timeout = timeout

    async def __aenter__(self):
        return self

    async def __aexit__(self, exc_type, exc_value, traceback):
        pass

    async def get(self, *args, **kwargs):
        if self.exception:
            raise self.exception

        if self.timeout:
            raise httpx.TimeoutException("Request timed out")

        return self.response


@pytest.mark.asyncio
async def test_get_weather_success(monkeypatch):
    weather_data = {
        "name": "Lahore",
        "main": {"temp": 32.5, "humidity": 45},
        "weather": [{"description": "clear sky"}],
    }

    saved_weather = {}

    async def mock_insert_one(document):
        saved_weather.update(document)

    monkeypatch.setattr(
        "app.services.weather.weather_collection.insert_one",
        mock_insert_one,
    )

    monkeypatch.setattr(
        "app.services.weather.httpx.AsyncClient",
        lambda *args, **kwargs: MockAsyncClient(
            response=MockResponse(data=weather_data)
        ),
    )

    service = WeatherService()
    result = await service.get_weather("Lahore")

    assert result["city"] == "Lahore"
    assert result["temperature"] == 32.5
    assert result["humidity"] == 45
    assert result["description"] == "clear sky"
    assert "searched_at" in result
    assert saved_weather["city"] == "Lahore"


@pytest.mark.asyncio
async def test_get_weather_city_not_found(monkeypatch):
    monkeypatch.setattr(
        "app.services.weather.httpx.AsyncClient",
        lambda *args, **kwargs: MockAsyncClient(
            response=MockResponse(status_code=404)
        ),
    )

    service = WeatherService()

    with pytest.raises(WeatherServiceCityNotFoundError):
        await service.get_weather("UnknownCity")


@pytest.mark.asyncio
async def test_get_weather_timeout(monkeypatch):
    monkeypatch.setattr(
        "app.services.weather.httpx.AsyncClient",
        lambda *args, **kwargs: MockAsyncClient(timeout=True),
    )

    service = WeatherService()

    with pytest.raises(WeatherServiceTimeoutError):
        await service.get_weather("Lahore")


@pytest.mark.asyncio
async def test_get_weather_connection_error(monkeypatch):
    request = httpx.Request("GET", "https://example.com")
    connection_error = httpx.RequestError(
        "Connection failed",
        request=request,
    )

    monkeypatch.setattr(
        "app.services.weather.httpx.AsyncClient",
        lambda *args, **kwargs: MockAsyncClient(
            exception=connection_error
        ),
    )

    service = WeatherService()

    with pytest.raises(WeatherServiceConnectionError):
        await service.get_weather("Lahore")


@pytest.mark.asyncio
async def test_get_weather_database_error(monkeypatch):
    weather_data = {
        "name": "Lahore",
        "main": {"temp": 32.5, "humidity": 45},
        "weather": [{"description": "clear sky"}],
    }

    async def mock_insert_one(document):
        raise Exception("Database connection failed")

    monkeypatch.setattr(
        "app.services.weather.weather_collection.insert_one",
        mock_insert_one,
    )

    monkeypatch.setattr(
        "app.services.weather.httpx.AsyncClient",
        lambda *args, **kwargs: MockAsyncClient(
            response=MockResponse(data=weather_data)
        ),
    )

    service = WeatherService()

    with pytest.raises(WeatherDatabaseError):
        await service.get_weather("Lahore")
