from abc import ABC, abstractmethod
from typing import TypeVar, override

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import insert, update


T = TypeVar("T")


class IRepository(ABC):
    @abstractmethod
    async def create_one(self, data: dict) -> T | None:
        pass

    @abstractmethod
    async def update_one(self, data: dict) -> T | None:
        pass


class BaseRepository(IRepository):
    model: type[T]

    def __init__(self, session: AsyncSession):
        self.session: AsyncSession = session

    @override
    async def create_one(self, data: dict) -> T | None:
        stmt = insert(self.model).values(**data).returning(self.model)
        res = await self.session.execute(stmt)
        return res.scalar_one_or_none()

    @override
    async def update_one(self, data: dict) -> T | None:
        stmt = (
            update(self.model)
            .values(**data)
            .where(self.model.id == data.get("id"))
            .returning(self.model)
        )
        res = await self.session.execute(stmt)
        return res.scalar_one_or_none()
