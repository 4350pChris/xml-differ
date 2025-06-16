from fastapi import FastAPI, Depends
from typing import Annotated
from .dependencies import diff_files
import uvicorn

app = FastAPI()


def diff_to_dict(diff: dict) -> dict:
    """Convert a diff object to a dictionary."""
    edits = diff['diff']
    return {
        'left_index': diff['left_index'],
        'right_index': diff['right_index'],
        'edits': [{
            'action': type(d).__name__,
            **d._asdict()
        } for d in edits]
    }


@app.post("/diff/")
async def diff_files(diffs: Annotated[list, Depends(diff_files)]):
    return {
        'diff': [diff_to_dict(diff) for diff in diffs],
    }

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
