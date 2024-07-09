from enum import StrEnum
from typing import TypeVar, Generic

from pydantic import BaseModel, computed_field, Field

from src import config

T = TypeVar("T")


class SortDirection(StrEnum):
    ASC = "asc"
    DESC = "desc"


class ListInput(BaseModel):
    search: str | None = None
    page: int = 1
    per_page: int = config.DEFAULT_PAGINATION_SIZE
    sort: str | None = None
    direction: SortDirection = SortDirection.ASC


class ListOutputMeta(BaseModel):
    page: int = 1
    per_page: int = config.DEFAULT_PAGINATION_SIZE
    total_count: int = 0

    @computed_field
    def next_page(self) -> int | None:
        next_page = self.page + 1
        return next_page if self.total_count > self.page * self.per_page else None


class ListOutput(BaseModel, Generic[T]):
    data: list[T] = Field(default_factory=list)
    meta: ListOutputMeta = Field(default_factory=ListOutputMeta)
