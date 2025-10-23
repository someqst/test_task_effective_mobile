from abc import ABC, abstractmethod

from database.core import SESSION_MAKER
from database.repositories import UserRepository


class IUnitOfWork(ABC):
    user: UserRepository


    @abstractmethod
    async def __aenter__(self):
        pass

    @abstractmethod
    async def __aexit__(self):
        pass

    @abstractmethod
    async def rollback(self):
        pass

    @abstractmethod
    async def commit(self):
        pass



class UnitOfWotk(IUnitOfWork):
    def __init__(self):
        self.session_maker = SESSION_MAKER

    async def __aenter__(self):
        self.session = self.session_maker()
        self.user = UserRepository(self.session)

    async def __aexit__(self, *args):
        await self.rollback()

    async def commit(self):
        await self.session.commit()

    async def rollback(self):
        await self.session.rollback()