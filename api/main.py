import logging
from contextlib import asynccontextmanager
from typing import Annotated

import uvicorn
from fastapi import FastAPI, status
from fastapi.params import Depends
from fastapi.middleware.cors import CORSMiddleware
from rq import Queue

from db.connection import close_db, init_db
from dependencies import get_queue
from routers import diff, laws, paragraphs
from worker.tasks import run_import

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)


@asynccontextmanager
async def lifespan(app: FastAPI):
    mongo_client = await init_db()

    yield

    close_db(mongo_client)


app = FastAPI(
    lifespan=lifespan,
    title="XML Diff API",
    description="API for comparing XML files of German laws",
)

origins = [
    "http://localhost",
    "http://localhost:5173",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(laws.router)
app.include_router(paragraphs.router)
app.include_router(diff.router)


@app.post("/import", status_code=status.HTTP_202_ACCEPTED)
async def start_work(queue: Annotated[Queue, Depends(get_queue)]):
    queue.enqueue(run_import, job_timeout="3h")
    return {"message": "Work started successfully"}


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
