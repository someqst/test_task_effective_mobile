from sqlalchemy import update, select

from database.models import User
from database.repositories.base_repository import BaseRepository


class UserRepository(BaseRepository):
    model: User = User

    async def delete_one(self, data: dict) -> User | None:
        stmt = (
            update(User).values(is_active=False).where(User.email == data.get("email")).returning(User)
        )
        res = await self.session.execute(stmt)
        return res.scalar_one_or_none()


    async def get_one(self, data: dict) -> User | None:
        stmt = select(User).where(User.email == data.get('email'))
        res = await self.session.execute(stmt)
        return res.scalar_one_or_none()