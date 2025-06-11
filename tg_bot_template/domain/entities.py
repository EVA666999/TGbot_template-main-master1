from sqlalchemy.orm import DeclarativeBase
from sqlalchemy import Column, Integer, String, BigInteger

class Base(DeclarativeBase):
    """Базовый класс для всех моделей SQLAlchemy"""
    pass

class User(Base):
    """Модель пользователя"""
    __tablename__ = "users"

    id = Column(BigInteger, primary_key=True)
    social_id = Column(BigInteger, nullable=True)
    name = Column(String, nullable=False)
    info = Column(String, nullable=True)
    taps = Column(Integer, default=0)

    def __repr__(self):
        return f"<User(id={self.id}, name='{self.name}', taps={self.taps})>" 
