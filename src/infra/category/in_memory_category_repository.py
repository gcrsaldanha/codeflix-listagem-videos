from src.domain.category.category import Category
from src.domain.category.category_repository import CategoryRepository


class InMemoryCategoryRepository(CategoryRepository):
    def __init__(self, categories: list[Category] = None):
        self.categories: list[Category] = categories or []

    def save(self, category: Category) -> None:
        if category not in self.categories:
            self.categories.append(category)
        else:
            self.categories[self.categories.index(category)] = category

    def list(self, query: str = "") -> list[Category]:
        return [category for category in self.categories]
