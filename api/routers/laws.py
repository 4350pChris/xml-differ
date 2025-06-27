from beanie import PydanticObjectId
from fastapi import APIRouter, HTTPException

from db.models import Law
from routers.response_models import (
    LawListProjection,
    PaginatedLawCollection,
    LawDetailProjection,
)

router = APIRouter(
    prefix="/laws",
    tags=["laws"],
    responses={404: {"description": "Not found"}},
)


@router.get(
    "/",
    response_description="List of laws",
    response_model=PaginatedLawCollection,
)
async def get_laws(page: int = 1, limit: int = 100):
    skip = (page - 1) * limit
    laws = (
        await Law.find_all()
        .skip(skip)
        .limit(limit)
        .project(LawListProjection)
        .to_list()
    )
    total = await Law.count()
    return PaginatedLawCollection(laws=laws, total=total, page=page, limit=limit)


@router.get("/{law_id}", response_model=LawDetailProjection)
async def get_law(law_id: PydanticObjectId):
    law = await Law.get(
        law_id, fetch_links=True, nesting_depth=1, projection_model=LawDetailProjection
    )
    if not law:
        raise HTTPException(status_code=404, detail="Law not found")
    return law
