from typing import Annotated

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
):
    left = await LawVersion.get(left_version_id, fetch_links=True)
    if left is None:
        raise HTTPException(status_code=404, detail="Left version not found")
    right = await LawVersion.get(right_version_id, fetch_links=True)
    if right is None:
        raise HTTPException(status_code=404, detail="Right version not found")

    diffs = []
    for paragraph in left.paragraphs:
        matching_paragraph = next(
            p for p in right.paragraphs if p.title == paragraph.title
        )
        if matching_paragraph:
            edits = diff_strategy(paragraph.content, matching_paragraph.content)
            diffs.append(
                Diff(
                    left_index=paragraph.index,
                    right_index=matching_paragraph.index,
                    edits=edits,
                )
            )

    return diffs
