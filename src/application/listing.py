from abc import ABC
from dataclasses import dataclass, field
from typing import TypeVar, Generic

from src import config

T = TypeVar("T")

# TODO: use pydantic for validation of input params
# TODO: inherit ListInput for each class to get proper input params


@dataclass
class ListInput:
    search: str | None = None
    page: int = 1
    per_page: int = 10
    sort: str | None = None
    direction: str = "asc"


@dataclass
class ListOutputMeta:
    page: int = 1
    per_page: int = config.DEFAULT_PAGINATION_SIZE
    next_page: int | None = None
    total_count: int = 0


@dataclass
class ListOutput(Generic[T], ABC):
    data: list[T] = field(default_factory=list)
    meta: ListOutputMeta = field(default_factory=ListOutputMeta)
