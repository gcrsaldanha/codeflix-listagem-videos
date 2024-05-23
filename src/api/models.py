import uuid
from datetime import datetime

from pydantic import BaseModel


class Category(BaseModel):  # TODO: create from Domain Model / Output
    id: uuid.UUID
    name: str
    description: str
    is_active: bool
    created_at: datetime
    updated_at: datetime
