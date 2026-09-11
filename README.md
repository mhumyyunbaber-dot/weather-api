# Weather API

A production-style Weather API built with FastAPI, MongoDB Atlas, and OpenWeather.

The API allows developers to fetch current weather data, store weather search history, manage API keys, monitor API usage, and access analytics.



 # Features

- Current weather data
- OpenWeather API integration
- MongoDB Atlas database
- Weather search history
- Pagination and filtering
- API key authentication
- Admin API key protection
- Rate limiting
- Request usage tracking
- API analytics
- Security headers
- CORS configuration
- Custom exception handling
- Logging
- Automated testing



 # Tech Stack

- Python
- FastAPI
- MongoDB Atlas
- OpenWeather API
- HTTPX
- Pytest
- SlowAPI

---

# Project Structure


weather-api/
│
├── app/
│   ├── api/
│   │   ├── analytics.py
│   │   ├── api_keys.py
│   │   ├── routes.py
│   │   └── usage.py
│   │
│   ├── core/
│   │   ├── admin_security.py
│   │   ├── limiter.py
│   │   ├── security.py
│   │   ├── security_headers.py
│   │   └── usage_tracking.py
│   │
│   ├── models/
│   │   ├── api_key.py
│   │   ├── usage.py
│   │   └── weather.py
│   │
│   ├── services/
│   │   ├── analytics.py
│   │   ├── api_keys.py
│   │   ├── usage.py
│   │   └── weather.py
│   │
│   ├── config.py
│   ├── database.py
│   ├── logging_config.py
│   ├── main.py
│   └── schemas.py
│
├── tests/
│   ├── test_api_key_routes.py
│   ├── test_api_keys.py
│   ├── test_weather_api.py
│   └── test_weather_service.py
│
├── .env.example
├── .gitignore
├── pytest.ini
├── requirements.txt
└── README.md
