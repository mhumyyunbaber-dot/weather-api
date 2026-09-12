# Weather API

A production-style Weather API built with FastAPI, MongoDB Atlas, and OpenWeather.

The API allows developers to fetch current weather data, store weather search history, manage API keys, monitor API usage, and access analytics.

## Features

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
- Docker support

## Tech Stack

- Python
- FastAPI
- MongoDB Atlas
- OpenWeather API
- HTTPX
- Pytest
- SlowAPI
- Docker

## Project Structure

```text
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
├── .dockerignore
├── .env.example
├── .gitignore
├── Dockerfile
├── pytest.ini
├── requirements.txt
└── README.md
```

## API Endpoints

### Weather

| Method | Endpoint | Description |
|---|---|---|
| POST | `/api/weather/` | Fetch current weather |
| GET | `/api/weather/history` | Get weather search history |

### API Keys

| Method | Endpoint | Description |
|---|---|---|
| POST | `/api/keys/create` | Create API key |
| GET | `/api/keys` | Get API keys |

### Analytics

| Method | Endpoint | Description |
|---|---|---|
| GET | `/api/analytics/usage` | Get usage summary |
| GET | `/api/analytics/endpoints` | Get endpoint usage analytics |

## Installation

### Clone the Repository

```bash
git clone https://github.com/mhumyyunbaber-dot/weather-api.git
```

```bash
cd weather-api
```

### Create Virtual Environment

```bash
python -m venv .venv
```

### Activate Virtual Environment

Windows:

```bash
.venv\Scripts\activate
```

### Install Dependencies

```bash
pip install -r requirements.txt
```

## Environment Variables

Create a `.env` file based on `.env.example`.

Example:

```env
MONGODB_URL=your_mongodb_connection_string
DATABASE_NAME=weather_api

WEATHER_API_KEY=your_openweather_api_key
WEATHER_API_URL=your_openweather_api_url

API_KEY=your_api_key
ADMIN_API_KEY=your_admin_api_key

ALLOWED_ORIGINS=http://localhost:3000
```

## Run the Application

```bash
uvicorn app.main:app --reload
```

The API will be available at:

```text
http://127.0.0.1:8000
```

Swagger documentation:

```text
http://127.0.0.1:8000/docs
```

## Running Tests

Run:

```bash
pytest
```

Current test status:

```text
24 passed
```

## Docker

### Build the Docker Image

```bash
docker build -t weather-api .
```

### Run the Container

```bash
docker run --env-file .env -p 8000:8000 --name weather-api-container weather-api
```

### Check Running Containers

```bash
docker ps
```

### Stop the Container

```bash
docker stop weather-api-container
```

## Security

The API includes:

- API key authentication
- Admin API key protection
- Rate limiting
- Security headers
- CORS configuration
- Environment-based secrets

## Analytics

The API tracks request activity including:

- Total requests
- Successful requests
- Failed requests
- Response time
- Endpoint usage

## Author

Built as a backend portfolio project using FastAPI and MongoDB Atlas.