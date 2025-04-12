from fastapi import APIRouter, status, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from db.db_connect import get_db
from engine.auth_managers import AuthManager
from models.auth_model import UserLogin, UserRegister


user_router = APIRouter(tags=["user"])


@user_router.post("/login", status_code=status.HTTP_200_OK)
async def login(user: UserLogin, session: AsyncSession = Depends(get_db)):
    token = await AuthManager().login(user, session)
    return token


@user_router.post("/register",status_code=status.HTTP_201_CREATED)
async def register(user: UserRegister, session: AsyncSession = Depends(get_db)):
    token = await AuthManager().register(user, session)
    return token
