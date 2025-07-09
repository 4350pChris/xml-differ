import logging
import os
from contextlib import asynccontextmanager
from typing import Annotated

import uvicorn
from fastapi import FastAPI, status
from fastapi.params import Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend
from rq import Queue

from db.connection import close_db, init_db
from dependencies import get_queue, get_async_redis_connection
from routers import diff, laws, paragraphs
from worker.tasks import run_import

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)

# Environment variables
MONGO_CONNECTION_STRING = os.environ.get("MONGODB_URI")
CORS_ORIGINS = os.environ.get(
    "CORS_ORIGINS", "http://localhost,http://localhost:5173"
).split(",")


@asynccontextmanager
async def lifespan(_: FastAPI):
    mongo_client = await init_db(MONGO_CONNECTION_STRING)
    redis_conn = get_async_redis_connection()
    FastAPICache.init(RedisBackend(redis_conn), prefix="fastapi-cache")

    yield

    close_db(mongo_client)


app = FastAPI(
    lifespan=lifespan,
    title="XML Diff API",
    description="API for comparing XML files of German laws",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=CORS_ORIGINS,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(laws.router)
app.include_router(paragraphs.router)
app.include_router(diff.router)


@app.post("/import", status_code=status.HTTP_202_ACCEPTED)
async def start_work(queue: Annotated[Queue, Depends(get_queue)]):
    queue.enqueue(run_import, MONGO_CONNECTION_STRING, job_timeout="6h")
    return {"message": "Work started successfully"}


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
