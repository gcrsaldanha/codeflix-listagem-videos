import uuid
from datetime import datetime

from pydantic import BaseModel


class Category(BaseModel):  # TODO: not FastAPI only
    id: uuid.UUID
    name: str
    description: str
    is_active: bool
    created_at: datetime
    updated_at: datetime
