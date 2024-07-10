from enum import StrEnum
from typing import Type

from src.application.list_entity import ListEntity, T
from src.application.listing import ListOutput, ListInput
from src.domain.category.category import Category
from src.domain.category.category_repository import CategoryRepository


class SortableFields(StrEnum):
    NAME = "name"
    DESCRIPTION = "description"


class ListCategory(ListEntity[Category, CategoryRepository]):
    class Input(ListInput):
        sort: SortableFields = SortableFields.NAME

    class Output(ListOutput[Category]):
        pass

    @property
    def output(self) -> Type[ListOutput[Category]]:
        return ListCategory.Output
