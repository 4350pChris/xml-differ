import os
from typing import Annotated

from fastapi.params import Depends
from rq import Queue

from redis import Redis


def get_redis_connection() -> Redis:
    redis_url = os.environ.get("REDIS_URL")
    if not redis_url:
        raise ValueError("REDIS_URL environment variable is not set")
    return Redis.from_url(redis_url)


def get_queue(redis_conn: Annotated[Redis, Depends(get_redis_connection)]):
    return Queue(connection=redis_conn)
