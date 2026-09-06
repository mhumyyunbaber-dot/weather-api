from fastapi import FastAPI

from app.api.routes import router
from app.logging_config import setup_logging


setup_logging()

app = FastAPI(
    title="Weather API",
    description="Professional weather microservice built with FastAPI and MongoDB Atlas.",
    version="1.0.0"
)


app.include_router(
    router,
    prefix="/api"
)


@app.get("/")
async def root():
    return {
        "message": "Weather API is running",
        "version": "1.0.0"
    }