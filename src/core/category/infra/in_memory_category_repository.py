from uuid import UUID
from src.core.category.domain.category_repository import CategoryRepository
from src.core.category.domain.category import Category


class InMemoryCategoryRepository(CategoryRepository):
    def __init__(self, categories: list[Category]=None):
        self.categories: list[Category] = categories or []

    def save(self, category: Category) -> None:
        self.categories.append(category)

    def list(self) -> list[Category]:
        return [category for category in self.categories]
