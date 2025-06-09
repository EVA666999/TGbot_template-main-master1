from sqlalchemy.orm import declarative_base, Mapped, mapped_column
from sqlalchemy import BigInteger

Base = declarative_base()

class UserModel(Base):
    """SQLAlchemy-модель пользователя."""
    __tablename__ = "users"
    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    name: Mapped[str]
    info: Mapped[str]
    social_id: Mapped[int | None] = mapped_column(BigInteger, nullable=True)
    taps: Mapped[int] = mapped_column(BigInteger, nullable=False, default=0, server_default="0") 