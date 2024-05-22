from abc import ABC
from dataclasses import dataclass, field
from typing import TypeVar, Generic

from src import config

T = TypeVar("T")


@dataclass
class ListOutputMeta:
    current_page: int = 1
    per_page: int = config.DEFAULT_PAGINATION_SIZE
    total: int = 0


@dataclass
class ListOutput(Generic[T], ABC):
    data: list[T] = field(default_factory=list)
    meta: ListOutputMeta = field(default_factory=ListOutputMeta)
