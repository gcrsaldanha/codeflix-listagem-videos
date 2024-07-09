from typing import List

from src.application.listing import SortDirection
from src.config import DEFAULT_PAGINATION_SIZE
from src.domain.category.category import Category
from src.domain.category.category_repository import CategoryRepository


class InMemoryCategoryRepository(CategoryRepository):
    def __init__(self, categories: list[Category] | None = None):
        self.categories: list[Category] = categories or []

    def save(self, category: Category) -> None:
        if category not in self.categories:
            self.categories.append(category)
        else:
            self.categories[self.categories.index(category)] = category

    def search(
        self,
        page: int = 1,
        per_page: int = DEFAULT_PAGINATION_SIZE,
        search: str | None = None,
        sort: str | None = None,
        direction: SortDirection = SortDirection.ASC,
    ) -> tuple[list[Category], int]:
        categories: List[Category] = [cat for cat in self.categories]
        total_count = len(categories)

        if search:
            categories = [
                cat
                for cat in categories
                if search.upper() in cat.name.upper() or search.upper() in cat.description.upper()
            ]

        if sort:
            categories = sorted(categories, key=lambda cat: getattr(cat, sort), reverse=direction == SortDirection.DESC)

        categories_page = categories[(page - 1) * per_page : (page * per_page)]
        return categories_page, total_count
