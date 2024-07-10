from enum import StrEnum
from typing import Type

from src.application.list_entity import ListEntity
from src.application.listing import ListOutput, ListInput
from src.domain.genre.genre import Genre
from src.domain.genre.genre_repository import GenreRepository


class SortableFields(StrEnum):
    NAME = "name"


class ListGenre(ListEntity[Genre, GenreRepository]):
    class Input(ListInput):
        sort: SortableFields = SortableFields.NAME

    class Output(ListOutput[Genre]):
        pass

    @property
    def output(self) -> Type[ListOutput[Genre]]:
        return ListGenre.Output
