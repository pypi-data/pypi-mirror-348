from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import Optional

class Settings(BaseSettings):
    APP_NAME: str = "Fitness App"
    API_V1_STR: str = "/api"
    SECRET_KEY: str
            
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 7
    ALGORITHM: str = "HS256"

    DATABASE_URL: str

    REDIS_URL: str

    TELEGRAM_BOT_TOKEN: Optional[str] = None

    WEBAPP_BASE_URL: str = "http://localhost"

    CORS_ORIGINS: list[str] = ["*"]

    model_config = SettingsConfigDict(
        env_file=".env",
        case_sensitive=True,
        extra='ignore' 
    )
settings = Settings()

