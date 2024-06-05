from dataclasses import dataclass
from datetime import datetime
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
        created_at: datetime
        updated_at: datetime

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
        # TODO: order in repository
        ordered_categories = sorted(
            categories,
            key=lambda category: getattr(category, input.order_by),
        )
        page_offset = (input.current_page - 1) * config.DEFAULT_PAGINATION_SIZE
        categories_page = ordered_categories[page_offset : page_offset + config.DEFAULT_PAGINATION_SIZE]

        return self.Output(
            data=[
                self.CategoryOutput(
                    id=category.id,
                    name=category.name,
                    description=category.description,
                    is_active=category.is_active,
                    created_at=category.created_at,
                    updated_at=category.updated_at,
                )
                for category in categories_page
            ],
            meta=ListOutputMeta(
                current_page=input.current_page,
                per_page=config.DEFAULT_PAGINATION_SIZE,
                total=len(categories),
            ),
        )
