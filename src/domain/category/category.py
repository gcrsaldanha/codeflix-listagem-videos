from typing import Annotated

from pydantic import StringConstraints

from src.domain.entity import Entity


class Category(Entity):
    name: Annotated[str, StringConstraints(min_length=1, max_length=255)]
    description: Annotated[str, StringConstraints(min_length=0, max_length=1024)]

    @classmethod
    def from_dict(cls, data: dict) -> "Category":
        return cls(**data)

    def to_dict(self) -> dict:
        return self.model_dump()
