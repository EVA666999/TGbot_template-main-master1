from dataclasses import dataclass

@dataclass
class User:
    """Доменная сущность пользователя."""
    id: int
    name: str
    info: str 