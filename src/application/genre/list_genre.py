from enum import StrEnum

from src.application.list_entity import ListEntity
from src.application.listing import ListInput


class SortableFields(StrEnum):
    NAME = "name"


class ListGenre(ListEntity):
    class Input(ListInput):
        sort: SortableFields = SortableFields.NAME
