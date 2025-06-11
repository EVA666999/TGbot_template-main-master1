import pytest
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker
from sqlalchemy.pool import StaticPool
from httpx import AsyncClient
from sqlalchemy import text
from typing import AsyncGenerator

from tg_bot_template.app import app
from tg_bot_template.domain.entities import Base
from tg_bot_template.repo.unit_of_work import UnitOfWork

DATABASE_URL = "sqlite+aiosqlite:///:memory:"

# Создание асинхронного engine для тестовой БД
engine = create_async_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)

# Используем async_sessionmaker (SQLAlchemy 2.0+)
AsyncTestingSessionLocal = async_sessionmaker(
    bind=engine,
    expire_on_commit=False,
    class_=AsyncSession
)

@pytest.fixture(autouse=True)
async def create_test_tables() -> AsyncGenerator[None, None]:
    """Создаёт все таблицы в тестовой БД перед тестами и удаляет после."""
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)

@pytest.fixture
async def session() -> AsyncGenerator[AsyncSession, None]:
    """Асинхронная сессия для тестов. Очищает все таблицы перед каждым тестом."""
    async with AsyncTestingSessionLocal() as session:
        # Очищаем все таблицы
        for table in reversed(Base.metadata.sorted_tables):
            await session.execute(text(f"DELETE FROM {table.name}"))
        await session.commit()
        yield session

@pytest.fixture
async def client() -> AsyncGenerator[AsyncClient, None]:
    """Асинхронный HTTP-клиент для тестирования FastAPI."""
    async with AsyncClient(app=app, base_url="http://test") as ac:
        yield ac

@pytest.fixture(autouse=True)
async def override_session_factory(monkeypatch):
    """Переопределяет session_factory на тестовый для DI и FastAPI-приложения."""
    from tg_bot_template import di, app as fastapi_app
    monkeypatch.setattr(di, "session_factory", AsyncTestingSessionLocal)
    monkeypatch.setattr(fastapi_app, "session_factory", AsyncTestingSessionLocal)
    yield
