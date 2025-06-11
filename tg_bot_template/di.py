import os
from dotenv import load_dotenv
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from sqlalchemy.pool import AsyncAdaptedQueuePool
from tg_bot_template.repo.unit_of_work import UnitOfWork
from tg_bot_template.domain.user_service import UserService
from tg_bot_template.domain.game_service import GameService

load_dotenv()  # Загружает переменные из .env

PG_HOST = os.environ["POSTGRES_HOST"]
PG_PORT = os.environ.get("POSTGRES_PORT", "5432")
PG_USER = os.environ["POSTGRES_USER"]
PG_PASSWORD = os.environ["POSTGRES_PASSWORD"]
PG_DB = os.environ["POSTGRES_DB"]

DATABASE_URL = (
    f"postgresql+asyncpg://{PG_USER}:{PG_PASSWORD}@{PG_HOST}:{PG_PORT}/{PG_DB}"
)

engine = create_async_engine(
    DATABASE_URL,
    echo=True,
    pool_pre_ping=True,
)

session_factory = async_sessionmaker(
    engine,
    expire_on_commit=False,
    class_=AsyncSession
)

uow = UnitOfWork(session_factory=session_factory)

def get_user_service() -> UserService:
    """DI-фабрика для UserService с UnitOfWork."""
    return UserService(uow)