from datetime import date
from typing import Optional, List

from beanie import PydanticObjectId

from pydantic import BaseModel, Field, ConfigDict


class ProjectionModel(BaseModel):
    id: Optional[PydanticObjectId] = Field(
        alias="_id", serialization_alias="id", default=None
    )
    model_config = ConfigDict(
        populate_by_name=True,
        arbitrary_types_allowed=True,
    )


class LawListProjection(ProjectionModel):
    name: str
    short_title: str | None = None
    long_title: str | None = None


class PaginatedLawCollection(BaseModel):
    laws: List[LawListProjection]
    total: int
    page: int
    limit: int

    @property
    def pages(self) -> int:
        return (self.total + self.limit - 1) // self.limit  # Ceiling division


class LawVersionProjection(ProjectionModel):
    date: date


class LawDetailProjection(LawListProjection):
    versions: List[LawVersionProjection] = Field(default_factory=list)
