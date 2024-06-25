from typing import TypeVar, Generic

from pydantic import BaseModel, field_serializer, Field
from pydantic_core.core_schema import SerializationInfo

from src import config

T = TypeVar("T")


class ListInput(BaseModel):
    search: str | None = None
    page: int = 1
    per_page: int = config.DEFAULT_PAGINATION_SIZE
    sort: str | None = None
    direction: str = "asc"  # TODO: constraint to asc or desc


class ListOutputMeta(BaseModel):
    page: int = 1
    per_page: int = config.DEFAULT_PAGINATION_SIZE
    next_page: int | None = None  # TODO: why can't I do Field(init=False)?
    total_count: int = 0

    @field_serializer("next_page")
    def serialize_next_page(self, value: None, _info: SerializationInfo) -> int | None:  # TODO: confirm signature
        return self.page + 1 if self.total_count > self.page * self.per_page else None


class ListOutput(BaseModel, Generic[T]):
    data: list[T] = Field(default_factory=list)
    meta: ListOutputMeta = Field(default_factory=ListOutputMeta)
