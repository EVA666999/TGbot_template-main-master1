from typing import Protocol, Dict

class IGameRepo(Protocol):
    async def get_taps(self, user_id: int) -> int: ...
    async def increment_taps(self, user_id: int) -> int: ...
    async def get_total_taps(self) -> int: ...

class GameService:
    """Сервис для игровой логики (нажатия кнопки, рейтинг)."""
    def __init__(self, game_repo: IGameRepo):
        self.game_repo = game_repo

    async def tap_button(self, user_id: int) -> int:
        """Увеличить счётчик нажатий пользователя и вернуть новое значение."""
        return await self.game_repo.increment_taps(user_id)

    async def get_user_taps(self, user_id: int) -> int:
        """Получить количество нажатий пользователя."""
        return await self.game_repo.get_taps(user_id)

    async def get_total_taps(self) -> int:
        """Получить общее количество нажатий всех пользователей."""
        return await self.game_repo.get_total_taps() 