from contextlib import asynccontextmanager

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from slowapi.errors import RateLimitExceeded
from slowapi.middleware import SlowAPIMiddleware
from slowapi import _rate_limit_exceeded_handler
from app.core.security_headers import SecurityHeadersMiddleware

from app.api.api_keys import router as api_keys_router
from app.api.routes import router
from app.config import settings
from app.core.limiter import limiter
from app.logging_config import setup_logging
from app.core.usage_tracking import UsageTrackingMiddleware
from app.api.analytics import router as analytics_router
from app.database import client


setup_logging()

@asynccontextmanager
async def lifespan(app: FastAPI):

    # Startup
    await client.admin.command("ping")
    print("MongoDB Atlas connection successful")

    yield

    # Shutdown
    await client.close()
    print("MongoDB connection closed")


app = FastAPI(
    title="Weather API",
    description="Professional weather microservice built with FastAPI and MongoDB Atlas.",
    version="1.0.0",
    lifespan=lifespan
)



allowed_origins = [
    origin.strip()
    for origin in settings.allowed_origins.split(",")
    if origin.strip()
]



app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,
    allow_credentials=False,
    allow_methods=["GET", "POST"],
    allow_headers=["Content-Type", "X-API-Key","X-Admin-API-Key"],
)



app.state.limiter = limiter

app.add_exception_handler(
    RateLimitExceeded,
    _rate_limit_exceeded_handler
)

app.add_middleware(
    SlowAPIMiddleware
)

app.add_middleware(
    SecurityHeadersMiddleware
)

app.add_middleware(
    UsageTrackingMiddleware
)

app.include_router(
    router,
    prefix="/api"
)

app.include_router(
    api_keys_router,
    prefix="/api"
)

app.include_router(
    analytics_router,
    prefix="/api"
)

@app.get("/")
@limiter.limit("30/minute")
async def root(request: Request):

    return {
        "message": "Weather API is running",
        "version": "1.0.0"
    }