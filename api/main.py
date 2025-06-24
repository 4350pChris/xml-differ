import logging
from contextlib import asynccontextmanager

import uvicorn
from fastapi import FastAPI, BackgroundTasks, status

from .db.connection import close_db, init_db
from .laws.repo import (
    clone_repo,
    repo_exists,
)
from .laws.importer import import_files
from .routers import laws, paragraphs, diff

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)


@asynccontextmanager
async def lifespan(app: FastAPI):
    if not repo_exists():
        clone_repo()
    mongo_client = await init_db()

    yield

    close_db(mongo_client)


app = FastAPI(
    lifespan=lifespan,
    title="XML Diff API",
    description="API for comparing XML files of German laws",
)

app.include_router(laws.router)
app.include_router(paragraphs.router)
app.include_router(diff.router)


@app.post("/import", status_code=status.HTTP_202_ACCEPTED)
async def start_work(background_tasks: BackgroundTasks):
    background_tasks.add_task(import_files)
    return {"message": "Work started successfully"}


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
