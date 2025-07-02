from functools import partial
from typing import List

from beanie import PydanticObjectId
from fastapi import APIRouter, HTTPException
from fastapi_cache.decorator import cache

from diff.differ import diff_files, XmlToHtmlDiffStrategy
from db.models import LawVersion

router = APIRouter(
    prefix="/diff",
    tags=["diff"],
    responses={404: {"description": "Not found"}},
)


@router.get(
    "/{left_version_id}/{right_version_id}", response_description="Diff endpoint"
)
@cache(expire=3600)
async def get_diff(
    left_version_id: PydanticObjectId,
    right_version_id: PydanticObjectId,
) -> List[str]:
    left = await LawVersion.get(left_version_id, fetch_links=True)
    if left is None:
        raise HTTPException(status_code=404, detail="Left version not found")

    right = await LawVersion.get(right_version_id, fetch_links=True)
    if right is None:
        raise HTTPException(status_code=404, detail="Right version not found")

    diff = partial(diff_files, XmlToHtmlDiffStrategy())
    matches = (
        (lp, rp) for lp in left.paragraphs for rp in right.paragraphs if lp.same_as(rp)
    )
    return [diff(left.content, right.content) for left, right in matches]
