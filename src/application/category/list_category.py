from dataclasses import dataclass
from uuid import UUID

from src import config
from src.application.listing import ListOutputMeta, ListOutput
from src.domain.category.category_repository import CategoryRepository


class ListCategory:
    @dataclass
    class CategoryOutput:
        id: UUID
        name: str
        description: str
        is_active: bool

    @dataclass
    class Input:
        order_by: str = "name"
        current_page: int = 1

    @dataclass
    class Output(ListOutput[CategoryOutput]):
        pass

    def __init__(self, repository: CategoryRepository) -> None:
        self.repository = repository

    def execute(self, input: Input) -> Output:
        categories = self.repository.list()
        ordered_categories = sorted(
            categories,
            key=lambda category: getattr(category, input.order_by),
        )
        page_offset = (input.current_page - 1) * config.DEFAULT_PAGINATION_SIZE
        categories_page = ordered_categories[page_offset:page_offset + config.DEFAULT_PAGINATION_SIZE]

        return self.Output(
            data=sorted(
                [
                    self.CategoryOutput(
                        id=category.id,
                        name=category.name,
                        description=category.description,
                        is_active=category.is_active,
                    ) for category in categories_page
                ],
                key=lambda category: getattr(category, input.order_by),
            ),
            meta=ListOutputMeta(
                current_page=input.current_page,
                per_page=config.DEFAULT_PAGINATION_SIZE,
                total=len(categories),
            ),
        )
