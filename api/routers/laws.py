from typing import List

from beanie import PydanticObjectId
from fastapi import APIRouter, HTTPException
from fastapi_cache.decorator import cache

from db.models import Law
from routers.response_models import (
    LawListProjection,
    LawDetailProjection,
)

router = APIRouter(
    prefix="/laws",
    tags=["laws"],
    responses={404: {"description": "Not found"}},
)


@router.get(
    "/", response_description="List of laws", response_model=List[LawListProjection]
)
@cache(expire=3600)
async def get_laws():
    laws = await Law.find_all().project(LawListProjection).to_list()
    return laws


@router.get("/{law_id}", response_model=LawDetailProjection)
@cache(expire=3600)
async def get_law(law_id: PydanticObjectId):
    law = await Law.get(
        law_id, fetch_links=True, nesting_depth=1, projection_model=LawDetailProjection
    )
    if not law:
        raise HTTPException(status_code=404, detail="Law not found")
    return law
