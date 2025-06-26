#!/usr/bin/env python
import os

from redis import Redis
from rq import Worker

if __name__ == "__main__":
    redis_url = os.environ.get("REDIS_URL")
    worker = Worker(["default"], connection=Redis.from_url(redis_url))
    worker.work()
