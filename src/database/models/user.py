import re

from sqlalchemy import BigInteger, Boolean, String
from sqlalchemy.orm import Mapped, mapped_column, validates

from database.models.base import Base

# Задание можно сделать через unit of work для масштабируемости,
# но поскольку мы работаем с одной сущностью (пользователь), необходимости в этом не вижу


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(
        BigInteger, autoincrement=True, primary_key=True, index=True
    )
    fullname: Mapped[str]
    email: Mapped[str] = mapped_column(String, index=True, unique=True)
    password: Mapped[str]
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    role: Mapped[int] = mapped_column(
        BigInteger, default=1
    )  # Можно через enum сделать, но пусть будет числовое просто

    @validates("email")
    def validate_email(self, key, email):
        if not email:
            raise ValueError("Email cannot be empty")

        pattern = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
        if not re.match(pattern, email):
            raise ValueError("Invalid email format")

        return email.lower()
