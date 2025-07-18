import hashlib
from functools import partial
from typing import List, Annotated

from beanie import PydanticObjectId
from fastapi import APIRouter, HTTPException, Request, Response
from fastapi.params import Depends
from fastapi_cache.decorator import cache

from diff.differ import (
    diff_files,
    XmlToHtmlDiffStrategy,
    DifferOptions,
    XmlToSplitHtmlDiffStrategy,
    DiffStrategy,
)
from db.models import LawVersion

router = APIRouter(
    prefix="/diff",
    tags=["diff"],
    responses={404: {"description": "Not found"}},
)


def get_diff_strategy(
    split: bool,
) -> XmlToHtmlDiffStrategy | XmlToSplitHtmlDiffStrategy:
    if split:
        return XmlToSplitHtmlDiffStrategy()
    return XmlToHtmlDiffStrategy()


def request_key_builder(
    func,
    namespace: str = "",
    *,
    request: Request = None,
    response: Response = None,
    args,
    kwargs,
):
    cache_key = hashlib.md5(
        ":".join(
            [
                namespace,
                request.method.lower(),
                request.url.path,
                repr(sorted(request.query_params.items())),
            ]
        ).encode()
    ).hexdigest()
    return f"{namespace}:{cache_key}"


@router.get(
    "/{left_version_id}/{right_version_id}", response_description="Diff endpoint"
)
@cache(expire=3600, key_builder=request_key_builder)
async def get_diff(
    left_version_id: PydanticObjectId,
    right_version_id: PydanticObjectId,
    options: Annotated[DifferOptions, Depends(DifferOptions)],
    strategy: Annotated[DiffStrategy, Depends(get_diff_strategy)],
) -> List[List[str]]:
    left = await LawVersion.get(left_version_id, fetch_links=True)
    if left is None:
        raise HTTPException(status_code=404, detail="Left version not found")

    right = await LawVersion.get(right_version_id, fetch_links=True)
    if right is None:
        raise HTTPException(status_code=404, detail="Right version not found")

    diff = partial(diff_files, strategy, options)
    matches = (
        (lp, rp) for lp in left.paragraphs for rp in right.paragraphs if lp.same_as(rp)
    )
    return [diff(left.content, right.content) for left, right in matches]
