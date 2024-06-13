import uuid
from datetime import datetime
from typing import TypeVar, Generic

from pydantic import BaseModel


class ListMeta(BaseModel):
    search: str | None = None
    page: int = 1
    per_page: int = 10
    sort: str | None = None
    direction: str = "asc"


class ListOutput(BaseModel):
    data: list[BaseModel]
    meta: ListMeta


class Category(BaseModel):  # TODO: create from Domain Model / Output
    id: uuid.UUID
    name: str
    description: str
    is_active: bool
    created_at: datetime
    updated_at: datetime
