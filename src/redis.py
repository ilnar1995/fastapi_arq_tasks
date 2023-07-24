from datetime import datetime, timedelta

from arq import ArqRedis
from arq import create_pool
from contextlib import asynccontextmanager
from typing import AsyncGenerator, Optional
from src.config import REDIS_HOST
from arq.connections import RedisSettings


@asynccontextmanager
async def get_redis(host: str = REDIS_HOST) -> AsyncGenerator[ArqRedis, None]:
    redis: Optional[ArqRedis] = None

    try:
        redis = await create_pool(RedisSettings(host), default_queue_name='high')
        yield redis
    finally:
        if redis is None:
            return

        await redis.close()


async def get_async_redis() -> AsyncGenerator[ArqRedis, None]:
    async with get_redis(host='redis_fastapi') as session:
        yield session
