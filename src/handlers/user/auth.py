from fastapi import APIRouter, Response, Request, Depends
from fastapi.exceptions import HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from data.create_user_form import CreateUserPost, LoginUserPost

from utils.depends import UserServiceDep


router = APIRouter()


@router.post("/register")
async def register_user(
    res: Response,
    user: CreateUserPost,
    user_service: UserServiceDep
):
    jwt_token = await user_service.create(user)
    res.set_cookie(
        key='jwt_token',
        value=jwt_token,
        httponly=True,
        #secure=True
    )

    return user


@router.post("/login")
async def login_user(
    res: Response,
    user: LoginUserPost,
    user_service: UserServiceDep
):
    
    unauth_exception = HTTPException(
        status_code=401,
        detail="invalid email or password"
    )

    jwt_token = await user_service.login_user(user, unauth_exception)

    res.set_cookie(
        key='jwt_token',
        value=jwt_token,
        httponly=True,
        #secure=True
    )
    
    return user


@router.delete("/delete")
async def delete_user(
    res: Response,
    user_service: UserServiceDep,
    credentials: HTTPAuthorizationCredentials = Depends(HTTPBearer())
):
    user = await user_service.delete_one(credentials.credentials)

    if not user:
        raise HTTPException(status_code=403)
    
    res.delete_cookie("jwt_token")


