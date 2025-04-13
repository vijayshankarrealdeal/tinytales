from fastapi import APIRouter, status, Depends, Request
from sqlalchemy.ext.asyncio import AsyncSession
from db.db_connect import get_db
from engine.auth_managers import AuthManager
from models.auth_model import UserLogin, UserRegister, UserResponse, UserUpdate
from engine.auth_managers import oauth2_scheme

user_router = APIRouter(tags=["user"])


@user_router.post("/login", status_code=status.HTTP_200_OK)
async def login(user: UserLogin, session: AsyncSession = Depends(get_db)):
    token = await AuthManager().login(user, session)
    return token


@user_router.post("/register", status_code=status.HTTP_201_CREATED)
async def register(user: UserRegister, session: AsyncSession = Depends(get_db)):
    token = await AuthManager().register(user, session)
    return token


@user_router.get(
    "/get_user",
    status_code=status.HTTP_200_OK,
    response_model=UserResponse,
    dependencies=[Depends(oauth2_scheme)],
)
async def get_user(request: Request, session: AsyncSession = Depends(get_db)):
    user_id = request.state.user.id
    user = await AuthManager().get_user(user_id, session)
    return user

@user_router.put(
    "/update_user",
    status_code=status.HTTP_200_OK,
    response_model=UserResponse,
    dependencies=[Depends(oauth2_scheme)],
)
async def update_user(
    user: UserUpdate, request: Request, session: AsyncSession = Depends(get_db)
):
    user_id = request.state.user.id
    user_data = await AuthManager().get_user(user_id, session)
    if not user_data:
        return {"message": "User not found"}
    user_data = await AuthManager().update_user(session, user, user_id)
    return user_data


@user_router.delete(
    "/delete_user",
    status_code=status.HTTP_200_OK,
    dependencies=[Depends(oauth2_scheme)],
)
async def delete_user(request: Request, session: AsyncSession = Depends(get_db)):
    user_id = request.state.user.id
    await AuthManager().delete_user(session, user_id)
    return {"message": "User deleted successfully"}
