from abc import ABC, abstractmethod
from typing import Tuple, List

from src.config import DEFAULT_PAGINATION_SIZE
from src.domain.category.category import Category


class CategoryRepository(ABC):
    @abstractmethod
    def save(self, category: Category):
        raise NotImplementedError

    @abstractmethod
    def search(
        self,
        page: int = 1,
        per_page: int = DEFAULT_PAGINATION_SIZE,
        search: str | None = None,
        sort: str | None = None,
        direction: str = "asc",
    ) -> Tuple[List[Category], int]:
        raise NotImplementedError

    def to_domain(self, data: dict) -> Category:
        return Category(
            id=data["id"],
            name=data["name"],
            description=data["description"],
            is_active=data["is_active"],
            created_at=data["created_at"],
            updated_at=data["updated_at"],
        )

    def from_domain(self, category: Category) -> dict:
        return {
            "id": category.id,
            "name": category.name,
            "description": category.description,
            "is_active": category.is_active,
            "created_at": category.created_at,
            "updated_at": category.updated_at,
        }
