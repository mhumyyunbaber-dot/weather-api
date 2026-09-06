# Weather API

A production-ready Weather API built with FastAPI that fetches weather data from OpenWeather and stores search history in MongoDB Atlas.

## Features

- Fetch current weather by city
- OpenWeather API integration
- MongoDB Atlas integration
- Weather search history
- Filter history by city
- Pagination
- Request validation
- Custom error handling
- Logging
- Unit testing
- API endpoint testing

## Tech Stack

- Python
- FastAPI
- MongoDB Atlas
- PyMongo Async
- HTTPX
- Pydantic
- Pytest

## Project Structure

```text
Wether/
│
├── app/
│   ├── api/
│   │   └── routes.py
│   │
│   ├── models/
│   │   └── weather.py
│   │
│   ├── services/
│   │   └── weather.py
│   │
│   ├── __init__.py
│   ├── config.py
│   ├── database.py
│   ├── schemas.py
│   └── main.py
│
├── tests/
│   ├── test_weather_api.py
│   └── test_weather_service.py
│
├── .env.example
├── .gitignore
├── pytest.ini
├── requirements.txt
└── README.md