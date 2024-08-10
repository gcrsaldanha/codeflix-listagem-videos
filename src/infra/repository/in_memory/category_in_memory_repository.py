from typing import List

from src.application.listing import SortDirection
from src.config import DEFAULT_PAGINATION_SIZE
from src.domain.category.category import Category
from src.domain.category.category_repository import CategoryRepository


class CategoryInMemoryRepository(CategoryRepository):
    def __init__(self, categories: list[Category] | None = None):
        self.categories: list[Category] = categories or []

    def save(self, entity: Category) -> None:
        if entity not in self.categories:
            self.categories.append(entity)
        else:
            self.categories[self.categories.index(entity)] = entity

    def search(
        self,
        page: int = 1,
        per_page: int = DEFAULT_PAGINATION_SIZE,
        search: str | None = None,
        sort: str | None = None,
        direction: SortDirection = SortDirection.ASC,
    ) -> tuple[list[Category], int]:
        categories: List[Category] = [category for category in self.categories]
        total_count = len(categories)

        if search:
            categories = [
                category
                for category in categories
                if search.upper() in category.name.upper() or search.upper() in category.description.upper()
            ]

        if sort:
            categories = sorted(
                categories, key=lambda category: getattr(category, sort), reverse=direction == SortDirection.DESC
            )

        ent_page = categories[(page - 1) * per_page : (page * per_page)]
        return ent_page, total_count
