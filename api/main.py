import logging
from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager
from typing import Annotated

import uvicorn
from fastapi import Depends, FastAPI, BackgroundTasks, status

from .db.models import Law
from .db.connection import close_db, init_db
from .dependencies import diffs_dep
from .diff.types import Diff
from .laws.repo import (
    clone_repo,
    repo_exists,
)
from .laws.importer import import_files
from .response_models import LawProjection, PaginatedLawCollection

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


@app.post("/diff/", response_model=list[Diff])
async def diff_files(diffs: Annotated[AsyncGenerator[Diff], Depends(diffs_dep)]):
    diffs_dicts = [diff async for diff in diffs]  # Collect all diffs into a list
    return diffs_dicts


@app.post("/import/", status_code=status.HTTP_202_ACCEPTED)
async def start_work(background_tasks: BackgroundTasks):
    background_tasks.add_task(import_files)
    return {"message": "Work started successfully"}


@app.get(
    "/laws/",
    response_description="List of laws",
    response_model=PaginatedLawCollection,
)
async def get_laws(page: int = 1, limit: int = 2):
    skip = (page - 1) * limit
    laws = await Law.find_all().skip(skip).limit(limit).project(LawProjection).to_list()
    total = await Law.count()
    return PaginatedLawCollection(laws=laws, total=total, page=page, limit=limit)


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
