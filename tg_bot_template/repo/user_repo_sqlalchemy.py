from typing import Optional
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import text
from tg_bot_template.domain.entities import User
from tg_bot_template.db_infra.models import UserModel

class UserRepoSQLAlchemy:
    """Реализация репозитория пользователя на SQLAlchemy (async)."""
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_by_id(self, user_id: int) -> Optional[User]:
        db_user = await self.session.get(UserModel, user_id)
        if db_user:
            return User(id=db_user.id, name=db_user.name, info=db_user.info)
        return None

    async def save(self, user: User) -> None:
        """Создать или обновить пользователя."""
        await self.session.execute(
            text("""
            INSERT INTO users (id, name, info, taps)
            VALUES (:id, :name, :info, 0)
            ON CONFLICT (id) DO UPDATE
            SET name = :name, info = :info
            """),
            {"id": user.id, "name": user.name, "info": user.info}
        )
        await self.session.commit() 