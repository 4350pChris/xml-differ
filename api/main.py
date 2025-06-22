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
from .laws.info import (
    clone_repo,
    repo_exists,
    get_all_file_paths,
    iter_laws,
)

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


async def import_file(file: str):
    laws_to_insert = []
    for law in iter_laws(file):
        existing_law = await Law.find_one(Law.name == law.name, Law.date == law.date)
        if existing_law is None:
            laws_to_insert.append(law)
    if laws_to_insert:
        await Law.insert_many(laws_to_insert)
        logging.info(
            f"Inserted {len(laws_to_insert)} new laws for {laws_to_insert[0].name}."
        )


@app.post("/import/", status_code=status.HTTP_202_ACCEPTED)
async def start_work(background_tasks: BackgroundTasks):
    files = get_all_file_paths()
    for file in files:
        background_tasks.add_task(import_file, file)
    return {"message": "Work started successfully"}


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
