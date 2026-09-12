from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    mongodb_url: str
    database_name: str

    weather_api_key: str
    weather_api_url: str

    api_key: str
    admin_api_key: str
    
    allowed_origins: str

    model_config = SettingsConfigDict(
        env_file=".env",
        case_sensitive=False
    )


settings = Settings()