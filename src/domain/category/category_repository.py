from abc import ABC, abstractmethod

from src.domain.category.category import Category


class CategoryRepository(ABC):
    @abstractmethod
    def save(self, category: Category):
        raise NotImplementedError

    @abstractmethod
    def list(self) -> list[Category]:
        raise NotImplementedError
