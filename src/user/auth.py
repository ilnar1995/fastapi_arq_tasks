from typing import Optional

from fastapi_users import FastAPIUsers
from fastapi import Request, Depends

from src.config import SECRET_AUTH
from src.core.db import get_db_session
from src.user.models import User, get_user_db
from src.user.schemas import UserCreate, UserRead
from fastapi_users.authentication import AuthenticationBackend, BearerTransport, JWTStrategy
from fastapi_users import BaseUserManager
from fastapi_users import (BaseUserManager, IntegerIDMixin, exceptions, models,
                           schemas)


class UserManager(IntegerIDMixin, BaseUserManager[User, int]):
    reset_password_token_secret = SECRET_AUTH
    verification_token_secret = SECRET_AUTH


bearer_transport = BearerTransport(tokenUrl="auth/jwt/login")


async def get_user_manager(user_db=Depends(get_user_db)):
    yield UserManager(user_db)


def get_jwt_strategy() -> JWTStrategy:
    return JWTStrategy(secret=SECRET_AUTH, lifetime_seconds=6600)


auth_backend = AuthenticationBackend(
    name="jwt",
    transport=bearer_transport,
    get_strategy=get_jwt_strategy,
)

fastapi_users = FastAPIUsers[User, int](
    get_user_manager,
    [auth_backend],
)

current_active_user = fastapi_users.current_user(active=True)
