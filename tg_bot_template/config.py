from pydantic_settings import BaseSettings
from functools import lru_cache
from typing import Optional

class Settings(BaseSettings):
    """Настройки приложения"""
    # Environment
    ENV: str = "dev"
    DEBUG: bool = True
    LOG_LEVEL: str = "DEBUG"
    LOG_PATH: str = "logs"
    LOG_ROTATION: str = "10 MB"
    LOG_RETENTION: str = "7 days"

    # Database settings
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_DB: str
    POSTGRES_HOST: str
    POSTGRES_PORT: str = "5432"
    DB_URL: str

    # Redis settings
    REDIS_URL: str
    FSM_REDIS_HOST: Optional[str] = None
    FSM_REDIS_DB: Optional[int] = None
    FSM_REDIS_PASS: Optional[str] = None
    FSM_STORAGE: str = "redis"

    # Telegram settings
    TG_BOT_TOKEN: str
    TG_WEBHOOK_TOKEN: str
    REGISTER_PASSPHRASE: Optional[str] = None
    CREATOR_ID: Optional[int] = None
    API_ID: str
    API_HASH: str

    # API settings
    API_HOST: str = "0.0.0.0"  # Слушаем все интерфейсы
    API_PORT: int = 8000

    class Config:
        env_file = ".env"
        case_sensitive = True
        extra = "allow"

@lru_cache()
def get_settings() -> Settings:
    """Получение настроек приложения"""
    return Settings()

settings = Settings()
