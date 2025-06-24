from typing import Annotated, List

from fastapi import APIRouter, HTTPException, Depends

from ..dependencies import get_diff_strategy
from ..diff.types import DiffStrategy, Diff
from ..db.models import LawVersion

router = APIRouter(
    prefix="/diff",
    tags=["diff"],
    responses={404: {"description": "Not found"}},
)


@router.get(
    "/{left_version_id}/{right_version_id}", response_description="Diff endpoint"
)
async def get_diff(
    left_version_id: str,
    right_version_id: str,
    diff_strategy: Annotated[DiffStrategy, Depends(get_diff_strategy)],
) -> List[Diff]:
    left = await LawVersion.get(left_version_id, fetch_links=True)
    if left is None:
        raise HTTPException(status_code=404, detail="Left version not found")
    right = await LawVersion.get(right_version_id, fetch_links=True)
    if right is None:
        raise HTTPException(status_code=404, detail="Right version not found")

    return [
        Diff(
            left_index=left.index,
            right_index=right.index,
            edits=diff_strategy(left.content, right.content),
        )
        for left in left.paragraphs
        for right in right.paragraphs
        if left.title == right.title
    ]
