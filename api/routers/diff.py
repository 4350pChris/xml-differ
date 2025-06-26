from typing import Annotated, List, Generator, Tuple

from fastapi import APIRouter, HTTPException, Depends

from ..dependencies import get_diff_strategy
from ..diff.types import DiffStrategy, Diff
from ..db.models import LawVersion, Paragraph

router = APIRouter(
    prefix="/diff",
    tags=["diff"],
    responses={404: {"description": "Not found"}},
)


async def get_matching_paragraphs(
    left_version_id: str,
    right_version_id: str,
) -> Generator[Tuple[Paragraph, Paragraph]]:
    left = await LawVersion.get(left_version_id, fetch_links=True)
    if left is None:
        raise HTTPException(status_code=404, detail="Left version not found")
    right = await LawVersion.get(right_version_id, fetch_links=True)
    if right is None:
        raise HTTPException(status_code=404, detail="Right version not found")
    return (
        (left, right)
        for left in left.paragraphs
        for right in right.paragraphs
        if left.same_as(right)
    )


@router.get(
    "/{left_version_id}/{right_version_id}", response_description="Diff endpoint"
)
async def get_diff(
    get_matching_paragraphs: Annotated[
        Generator[Paragraph], Depends(get_matching_paragraphs)
    ],
    diff_strategy: Annotated[DiffStrategy, Depends(get_diff_strategy)],
) -> List[Diff]:
    return [
        Diff(
            left_index=left.index,
            right_index=right.index,
            edits=diff_strategy(left.content, right.content),
        )
        for left, right in get_matching_paragraphs
    ]
