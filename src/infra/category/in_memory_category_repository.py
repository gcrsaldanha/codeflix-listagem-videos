from src.domain.category.category import Category
from src.domain.category.category_repository import CategoryRepository


class InMemoryCategoryRepository(CategoryRepository):
    def __init__(self, categories: list[Category] = None):
        self.categories: list[Category] = categories or []

    def save(self, category: Category) -> None:
        self.categories.append(category)

    def list(self) -> list[Category]:
        return [category for category in self.categories]
