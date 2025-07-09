import os
from typing import Annotated

from fastapi.params import Depends
from rq import Queue

from redis import Redis, asyncio as aioredis


def _get_redis_url() -> str:
    redis_url = os.environ.get("REDIS_URL")
    if not redis_url:
        raise ValueError("REDIS_URL environment variable is not set")
    return redis_url


def get_async_redis_connection() -> aioredis.Redis:
    return aioredis.from_url(_get_redis_url())


def get_redis_connection() -> Redis:
    return Redis.from_url(_get_redis_url())


def get_queue(redis_conn: Annotated[Redis, Depends(get_redis_connection)]):
    return Queue(connection=redis_conn)
