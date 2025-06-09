from tg_bot_template.repo.unit_of_work import UnitOfWork
from tg_bot_template.repo.user_repo_sqlalchemy import UserRepoSQLAlchemy
from tg_bot_template.domain.entities import User
from typing import Optional

class UserService:
    """Сервис для бизнес-логики пользователя через UoW и репозиторий."""
    def __init__(self, uow: UnitOfWork):
        self.uow = uow

    async def set_profile(self, user_id: int, name: str, info: str) -> None:
        """Создать или обновить профиль пользователя."""
        async with self.uow as session:
            repo = UserRepoSQLAlchemy(session)
            user = User(id=user_id, name=name, info=info)
            await repo.save(user)

    async def get_profile(self, user_id: int) -> Optional[User]:
        """Получить профиль пользователя по id."""
        async with self.uow as session:
            repo = UserRepoSQLAlchemy(session)
            return await repo.get_by_id(user_id) 