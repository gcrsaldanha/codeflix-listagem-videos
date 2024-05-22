import logging
import uuid
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from datetime import datetime
from uuid import UUID

from src.domain.notification import Notification

logger = logging.getLogger(__name__)


@dataclass(kw_only=True)
class Entity(ABC):
    id: UUID
    created_at: datetime
    updated_at: datetime
    notification: Notification = field(default_factory=Notification, init=False)

    def __eq__(self, other: "Entity") -> bool:
        if not isinstance(other, self.__class__):
            return False

        return self.id == other.id

    @abstractmethod
    def validate(self):
        pass
