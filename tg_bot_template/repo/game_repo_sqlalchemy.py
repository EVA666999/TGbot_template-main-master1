from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import text
from ..domain.game_service import IGameRepo

class GameRepoSQLAlchemy(IGameRepo):
    """Репозиторий для игровой логики через SQLAlchemy."""
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_taps(self, user_id: int) -> int:
        """Получить количество нажатий пользователя."""
        result = await self.session.execute(text("SELECT taps FROM users WHERE id = :user_id"), {"user_id": user_id})
        return result.scalar() or 0

    async def increment_taps(self, user_id: int) -> int:
        """Увеличить счётчик нажатий пользователя и вернуть новое значение."""
        await self.session.execute(text("UPDATE users SET taps = taps + 1 WHERE id = :user_id"), {"user_id": user_id})
        await self.session.commit()
        return await self.get_taps(user_id)

    async def get_total_taps(self) -> int:
        """Получить общее количество нажатий всех пользователей."""
        result = await self.session.execute(text("SELECT SUM(taps) FROM users"))
        return result.scalar() or 0 