from abc import ABC, abstractmethod
from typing import Tuple, List

from src.domain.category.category import Category


class CategoryRepository(ABC):
    @abstractmethod
    def save(self, category: Category):
        raise NotImplementedError

    @abstractmethod
    def list(self, query: str = "") -> list[Category]:
        raise NotImplementedError

    @abstractmethod
    def search(
        self,
        search: str | None,
        page: int,
        per_page: int,
        sort: str | None,
        direction: str,
    ) -> Tuple[List[Category], int]:
        raise NotImplementedError

    @abstractmethod
    def to_domain(self, data: dict) -> Category:
        raise NotImplementedError

    @abstractmethod
    def from_domain(self, category: Category) -> dict:
        raise NotImplementedError
