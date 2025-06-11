<<<<<<< HEAD
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
=======
from enum import Enum

from pydantic_settings import BaseSettings, SettingsConfigDict


class Envs(Enum):
    local_test = "local_test"
    stage = "stage"
    prod = "prod"


class BotSettings(BaseSettings):
    tg_bot_token: str = ""
    postgres_db: str = "postgres"
    postgres_user: str = "postgres"
    postgres_password: str = "postgres"
    postgres_host: str = "localhost"
    fsm_redis_host: str = "localhost"
    fsm_redis_db: int = 0
    fsm_redis_pass: str = ""
    register_passphrase: str = ""
    creator_id: str = ""
    db_host: str = "localhost"
    api_id: str = ""
    api_hash: str = ""
    main_project_path: str = ""

    environment: Envs = Envs.local_test

    inline_kb_button_row_width: int = 2
    schedule_healthcheck: str = "7:00"  # !!!UTC timezone!!!

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="allow")


settings = BotSettings()
>>>>>>> c0ce5bcc81f614ac8b3fb8fcde787513781c2614
