from typing import AsyncGenerator

from sqlalchemy import create_engine
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from starlette.requests import Request
from fastapi import Depends
from src.config import DB_HOST, DB_NAME, DB_PASS, DB_PORT, DB_USER


SQLALCHEMY_DATABASE_URL = f"postgresql+asyncpg://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

engine = create_async_engine(SQLALCHEMY_DATABASE_URL)
async_session_maker = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)

Base = declarative_base()


# Dependency
# вовращаем перемен db из request
async def get_db_session(request: Request):
    async with async_session_maker() as session:
        yield session




