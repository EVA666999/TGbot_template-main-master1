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
