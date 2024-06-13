from dataclasses import dataclass
from datetime import datetime
from uuid import UUID

from src import config
from src.application.listing import ListOutputMeta, ListOutput, ListInput
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
    class Input(ListInput):
        sort: str = "name"

    @dataclass
    class Output(ListOutput[CategoryOutput]):
        pass

    def __init__(self, repository: CategoryRepository) -> None:
        self.repository = repository

    # TODO: validate listing sort field
    def execute(self, input: Input) -> Output:
        categories, total_count = self.repository.search(
            search=input.search,
            page=input.page,
            per_page=input.per_page,
            sort=input.sort,
            direction=input.direction,
        )

        print(categories, total_count)
        next_page = input.page + 1 if total_count > input.page * input.per_page else None

        data = [
            self.CategoryOutput(
                id=category.id,
                name=category.name,
                description=category.description,
                is_active=category.is_active,
                created_at=category.created_at,
                updated_at=category.updated_at,
            )
            for category in categories
        ]
        meta = ListOutputMeta(
            page=input.page,
            per_page=input.per_page,
            next_page=next_page,
            total_count=total_count,
        )

        return ListCategory.Output(data=data, meta=meta)
