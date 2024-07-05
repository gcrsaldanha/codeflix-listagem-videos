from datetime import datetime, UTC
from typing import Annotated
from uuid import uuid4

from pydantic import StringConstraints

from src.domain.entity import Entity


class Category(Entity):
    name: Annotated[str, StringConstraints(min_length=1, max_length=255)]
    description: Annotated[str, StringConstraints(min_length=0, max_length=1024)]
