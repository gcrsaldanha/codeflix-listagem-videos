from typing import Annotated
from typing import Annotated
from uuid import UUID

from pydantic import StringConstraints

from src.domain.entity import Entity


class Genre(Entity):
    name: Annotated[str, StringConstraints(min_length=1, max_length=255)]
    categories: set[UUID] = set()

    @classmethod
    def from_dict(cls, data: dict) -> "Genre":
        return cls(**data)
