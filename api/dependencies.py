import os

from rq import Queue

from diff.differ import diff_files
from diff.xmldiff_strat import XmldiffStrategy
from functools import partial
from redis import Redis


def get_diff_strategy():
    return partial(diff_files, XmldiffStrategy())


def get_queue():
    redis_url = os.environ.get("REDIS_URL")
    if not redis_url:
        raise ValueError("REDIS_URL environment variable is not set")
    redis_conn = Redis.from_url(redis_url)
    return Queue(connection=redis_conn)
