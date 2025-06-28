from datetime import date
from typing import List

from beanie import PydanticObjectId
from bson import DBRef

from pydantic import BaseModel, Field, ConfigDict


class ProjectionModel(BaseModel):
    id: PydanticObjectId = Field(alias="_id", serialization_alias="id")
    model_config = ConfigDict(
        populate_by_name=True,
        arbitrary_types_allowed=True,
    )


class PaginatedCollection(BaseModel):
    total: int
    page: int
    limit: int

    @property
    def pages(self) -> int:
        return (self.total + self.limit - 1) // self.limit  # Ceiling division


class LawListProjection(ProjectionModel):
    name: str
    short_title: str | None = None
    long_title: str | None = None


class LawVersionListProjection(ProjectionModel):
    date: date


class LawDetailProjection(LawListProjection):
    versions: List[LawVersionListProjection]


class LawVersionDetailProjection(ProjectionModel):
    date: date
    paragraphs: List[DBRef]


class ParagraphProjection(ProjectionModel):
    index: int
    title: str
    content: str


class PaginatedParagraphCollection(PaginatedCollection):
    paragraphs: List[ParagraphProjection]
