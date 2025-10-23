from typing import Annotated
from fastapi import Depends

from services import UserService
from services.unit_of_work import UnitOfWotk, IUnitOfWork



async def get_user_service(uow: IUnitOfWork = Depends(UnitOfWotk)):
    return UserService(uow)


UserServiceDep = Annotated[UserService, Depends(get_user_service)]