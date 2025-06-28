from beanie import PydanticObjectId
from fastapi import APIRouter, HTTPException
from beanie.operators import In

from db.models import LawVersion, Paragraph
from routers.response_models import (
    PaginatedParagraphCollection,
    ParagraphProjection,
    LawVersionDetailProjection,
)

router = APIRouter(
    prefix="/versions/{version_id}/paragraphs",
    tags=["paragraphs"],
    responses={404: {"description": "Not found"}},
)


@router.get("/", response_description="List of paragraphs")
async def get_paragraphs(
    version_id: PydanticObjectId, page: int = 1, limit: int = 100
) -> PaginatedParagraphCollection:
    version: LawVersionDetailProjection | None = await LawVersion.get(
        version_id, projection_model=LawVersionDetailProjection
    )
    if not version:
        raise HTTPException(status_code=404, detail="Version not found")

    skip = (page - 1) * limit
    paragraph_ids = [p.id for p in version.paragraphs][skip : skip + limit]
    paragraphs = (
        await Paragraph.find(In(Paragraph.id, paragraph_ids))
        .project(ParagraphProjection)
        .to_list()
    )
    return PaginatedParagraphCollection(
        paragraphs=paragraphs, total=len(version.paragraphs), page=page, limit=limit
    )
