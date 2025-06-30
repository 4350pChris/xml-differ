import os

from rq import Queue

from redis import Redis


def get_queue():
    redis_url = os.environ.get("REDIS_URL")
    if not redis_url:
        raise ValueError("REDIS_URL environment variable is not set")
    redis_conn = Redis.from_url(redis_url)
    return Queue(connection=redis_conn)
