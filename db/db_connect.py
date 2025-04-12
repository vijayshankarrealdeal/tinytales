import os
from typing import AsyncGenerator
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker, declarative_base
from dotenv import load_dotenv

# Load environment variables if needed
load_dotenv()

DATABASE_URL = (
    f"postgresql+asyncpg://{os.environ.get('username', 'postgres')}:"
    f"{os.environ.get('password', '123')}@"
    f"{os.environ.get('hostname', 'localhost')}:"
    f"{os.environ.get('port', '5432')}/"
    f"{os.environ.get('database', 'child')}"
)

DATABASE_URL = "postgresql+asyncpg://tinytales_user:Vm8lSckECQl0EMr3KcCozFn9NMieZm9P@dpg-cvt43tqdbo4c73chu12g-a.oregon-postgres.render.com/tinytales"

# Create the async engine
engine = create_async_engine(DATABASE_URL, echo=True, future=True)

# Create a sessionmaker factory for AsyncSession
async_session = sessionmaker(
    engine, class_=AsyncSession, expire_on_commit=False
)
Base = declarative_base()

async def get_db() -> AsyncGenerator[AsyncSession, None]:
    async with async_session() as session:
        yield session