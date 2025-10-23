import jwt
from fastapi import HTTPException
from datetime import datetime, timedelta
from bcrypt import hashpw, gensalt, checkpw

from data.create_user_form import (CreateUserPost, UserFromDB,
                                   UserToDB, LoginUserPost)
from data.config import settings

from services.unit_of_work import IUnitOfWork


class UserService:
    def __init__(self, uow: IUnitOfWork) -> None:
        self.uow = uow
    
    async def create(self, user: CreateUserPost):

        password = hashpw(user.password.encode(), gensalt())
        user_to_db = UserToDB(fullname=user.fullname, email=user.email, password=password)

        async with self.uow:
            await self.uow.user.create_one(user_to_db.model_dump())
            await self.uow.commit()

        return jwt.encode(
            {
                "email": user.email,
                "expire_at": (datetime.now() + timedelta(days=30)).timestamp()
            },
            settings.PRIVATE_KEY.get_secret_value(),
            algorithm="HS256"
        )
    

    async def login_user(
            self, user: LoginUserPost,
            unauth_exception: HTTPException, 
    ):
        user_from_db = await self._get_user(user.model_dump())

        if not user_from_db:
            raise unauth_exception

        if not checkpw(user.password.encode(), user_from_db.password.encode()):
            raise unauth_exception
        
        if not user_from_db.is_active:
            raise HTTPException(status_code=403)

        return jwt.encode(
            {
                "email": user.email,
                "expire_at": (datetime.now() + timedelta(days=30)).timestamp()
            },
            settings.PRIVATE_KEY.get_secret_value(),
            algorithm="HS256"
        )


    async def delete_one(self, jwt_token: str):
        user = await self.get_uset_with_jwt(jwt_token)

        if not user.is_active:
            return False
        
        async with self.uow:
            user_from_db = await self.uow.user.delete_one(user.model_dump())
            user = UserFromDB.model_validate(user_from_db)
            await self.uow.commit()
        
        return user


    async def get_uset_with_jwt(self, jwt_token: str) -> UserFromDB:
        decoded_jwt = self._decode_jwt(jwt_token)

        return await self._get_user(decoded_jwt)


    def _decode_jwt(self, jwt_token: str):
        return jwt.decode(
            jwt_token,
            settings.PRIVATE_KEY.get_secret_value(),
            algorithms=["HS256"]
        )


    async def _get_user(self, user: dict) -> UserFromDB:
        async with self.uow:
            user_from_db = await self.uow.user.get_one(user)
            user = UserFromDB.model_validate(user_from_db)

        return user
