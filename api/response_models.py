from typing import Optional, List

from beanie import PydanticObjectId

from pydantic import BaseModel, Field, ConfigDict


class LawProjection(BaseModel):
    id: Optional[PydanticObjectId] = Field(
        alias="_id", serialization_alias="id", default=None
    )
    name: str
    short_title: str | None = None
    long_title: str | None = None
    model_config = ConfigDict(
        populate_by_name=True,
        arbitrary_types_allowed=True,
    )


class PaginatedLawCollection(BaseModel):
    laws: List[LawProjection]
    total: int
    page: int
    limit: int

    @property
    def pages(self) -> int:
        return (self.total + self.limit - 1) // self.limit  # Ceiling division
