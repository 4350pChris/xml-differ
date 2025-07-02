from functools import partial
from typing import Annotated, List, Generator, Tuple

from beanie import PydanticObjectId
from fastapi import APIRouter, HTTPException, Depends
from fastapi_cache.decorator import cache

from diff.differ import diff_files, XmlToHtmlDiffStrategy
from db.models import LawVersion, Paragraph

router = APIRouter(
    prefix="/diff",
    tags=["diff"],
    responses={404: {"description": "Not found"}},
)


async def get_matching_paragraphs(
    left_version_id: PydanticObjectId,
    right_version_id: PydanticObjectId,
) -> Generator[Tuple[Paragraph, Paragraph]]:
    left = await LawVersion.get(left_version_id, fetch_links=True)
    if left is None:
        raise HTTPException(status_code=404, detail="Left version not found")
    right = await LawVersion.get(right_version_id, fetch_links=True)
    if right is None:
        raise HTTPException(status_code=404, detail="Right version not found")
    return (
        (lp, rp) for lp in left.paragraphs for rp in right.paragraphs if lp.same_as(rp)
    )


def handle_html_diff(
    matching_paragraphs: Generator[Tuple[Paragraph, Paragraph]],
) -> List[str]:
    diff = partial(diff_files, XmlToHtmlDiffStrategy())
    return [diff(left.content, right.content) for left, right in matching_paragraphs]


@router.get(
    "/{left_version_id}/{right_version_id}", response_description="Diff endpoint"
)
@cache(expire=3600)
async def get_diff(
    matching_paragraphs: Annotated[
        Generator[Tuple[Paragraph, Paragraph]], Depends(get_matching_paragraphs)
    ],
) -> List[str]:
    return handle_html_diff(matching_paragraphs)
