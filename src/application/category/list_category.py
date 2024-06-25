from enum import StrEnum

from src.application.category.exceptions import SearchError
from src.application.listing import ListOutputMeta, ListOutput, ListInput
from src.domain.category.category import Category
from src.domain.category.category_repository import CategoryRepository


class SortableFields(StrEnum):
    name = "name"
    description = "description"


class ListCategory:
    class Input(ListInput):
        sort: SortableFields = SortableFields.name

    class Output(ListOutput[Category]):
        pass

    def __init__(self, repository: CategoryRepository) -> None:
        self.repository = repository

    def execute(self, input: Input) -> Output:
        try:
            categories, total_count = self.repository.search(
                search=input.search,
                page=input.page,
                per_page=input.per_page,
                sort=input.sort,
                direction=input.direction,
            )
        except Exception as err:
            raise SearchError(err)
        else:
            meta = ListOutputMeta(
                page=input.page,
                per_page=input.per_page,
                total_count=total_count,
            )
            return ListCategory.Output(data=categories, meta=meta)
