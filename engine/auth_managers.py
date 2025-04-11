from typing import Optional
import jwt
import datetime
from fastapi import Request
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from fastapi import HTTPException
from passlib.context import CryptContext
from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession

from db.db_models import User
from models.auth_model import UserLogin, UserRegister
from db.db_connect import async_session


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class Auth:
    @staticmethod
    def encode_token(user_data):
        payload = {
            "exp": datetime.datetime.now() + datetime.timedelta(days=12),
            "sub": str(user_data.id),
        }
        try:
            token = jwt.encode(payload, "XYZ", algorithm="HS256")
            return {"token": token}
        except Exception as e:
            raise HTTPException(status_code=400, detail="Unkonwn error")

    @staticmethod
    async def get_user(user_id, session):
        try:
            query = select(User).where(User.id == user_id)
            user_data = await session.execute(query)
            return user_data
        except HTTPException as e:
            raise HTTPException(status_code=400, detail="Unkonwn error")

    async def register(self, user_data: UserRegister, session: AsyncSession):
        user_data.password = pwd_context.hash(user_data.password)
        try:
            user_data = User(
                fullname=user_data.fullname,
                email=user_data.email,
                password=user_data.password,
            )
            session.add(user_data)
            await session.commit()
            await session.refresh(user_data)
            return self.encode_token(user_data)
        except HTTPException as e:
            session.rollback()

    async def login(self, user_data: UserLogin, session: AsyncSession):
        query = select(User).where(User.email == user_data.email)
        result = await session.execute(query)
        user_data_db = result.scalar_one_or_none()
        if not user_data_db:
            raise HTTPException(status_code=400, detail="Invalid email or password")
        if not pwd_context.verify(user_data.password, user_data_db.password):
            raise HTTPException(status_code=400, detail="Invalid email or password")
        return self.encode_token(user_data_db)


class CustomHTTPBearer(HTTPBearer):
    async def __call__(
        self, request: Request
    ) -> Optional[HTTPAuthorizationCredentials]:
        credentials: HTTPAuthorizationCredentials = await super().__call__(request)
        try:
            # Decode the token using the secret and algorithm.
            payload = jwt.decode(credentials.credentials, "XYZ", algorithms=["HS256"])
            user_id = int(payload["sub"])

            # Open a new asynchronous session to query for the user.
            async with async_session() as session:
                stmt = select(User).where(User.id == user_id)
                result = await session.execute(stmt)
                user_data = result.scalar_one_or_none()
                if not user_data:
                    raise HTTPException(
                        status_code=401, detail="Invalid token: user not found"
                    )

                # Attach the user data to the request state
                request.state.user = user_data

            # Return the original credentials (or you might return the payload)
            return credentials

        except jwt.ExpiredSignatureError:
            raise HTTPException(status_code=401, detail="Token expired")
        except jwt.InvalidTokenError:
            raise HTTPException(status_code=401, detail="Invalid token")


# Instantiate the custom security scheme.
oauth2_scheme = CustomHTTPBearer()


def is_admin(request):
    if request.state.user["user_type"] == "ADMIN":
        return True
    raise HTTPException(401, "You are not authorized.")
