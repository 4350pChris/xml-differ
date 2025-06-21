from collections.abc import AsyncGenerator

from fastapi import FastAPI, Depends
from typing import Annotated

from .diff.types import Diff
from .dependencies import diffs_dep
import uvicorn

app = FastAPI()

@app.post("/diff/", response_model=list[Diff])
async def diff_files(diffs: Annotated[AsyncGenerator[Diff], Depends(diffs_dep)]):
    diffs_dicts = [diff async for diff in diffs]  # Collect all diffs into a list
    return diffs_dicts

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
