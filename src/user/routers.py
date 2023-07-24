from typing import List

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.core.db import get_db_session
from src.user.auth import auth_backend, fastapi_users
from src.user.schemas import UserRead, UserCreate
from .models import User

auth_router = APIRouter()

auth_router.include_router(
    fastapi_users.get_auth_router(auth_backend),
    prefix="/auth/jwt",
    tags=["auth"],
)

auth_router.include_router(
    fastapi_users.get_register_router(UserRead, UserCreate),
    prefix="/auth",
    tags=["auth"],
)

user_router = APIRouter()


@user_router.get('/', status_code=201, response_model=List[UserRead])
async def get_users(db: AsyncSession = Depends(get_db_session)):
    """
    добавление или удаление пользователя в бан пользователя по id
    """
    user_db_instances = await User.get_all(db)

    users = [UserRead(
        id=user_db_instance.id,
        email=user_db_instance.email,
        username=user_db_instance.username,
        is_active=user_db_instance.is_active,
        is_banned=user_db_instance.is_banned,
        is_superuser=user_db_instance.is_superuser,
        is_verified=user_db_instance.is_verified) for user_db_instance in user_db_instances]
    return users
