import logging
from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict

logger = logging.getLogger(__name__)


class Entity(BaseModel):
    id: UUID
    created_at: datetime
    updated_at: datetime
    is_active: bool

    model_config = ConfigDict(extra="forbid", validate_assignment=True)

    def __eq__(self, value: object) -> bool:
        if isinstance(value, Entity):
            return self.id == value.id
        return False

    @classmethod
    def from_dict(cls, data: dict) -> "Entity":
        return cls(**data)

    def to_dict(self) -> dict:
        return self.model_dump()
