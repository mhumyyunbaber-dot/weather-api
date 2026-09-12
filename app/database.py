from pymongo import AsyncMongoClient

from app.config import settings


client = AsyncMongoClient(settings.mongodb_url)

database = client[settings.database_name]


weather_collection = database["weather"]

api_keys_collection = database["api_keys"]

usage_collection = database["api_usage"]