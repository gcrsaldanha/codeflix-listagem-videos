from abc import ABC, abstractmethod
from typing import TypeVar, Generic, Type

from src.application.exceptions import SearchError
from src.application.listing import ListInput, ListOutput, ListOutputMeta
from src.domain.entity import Entity
from src.domain.repository import Repository

T = TypeVar("T", bound=Entity)
R = TypeVar("R", bound=Repository)


class ListEntity(Generic[T, R], ABC):
    def __init__(self, repository: R) -> None:
        self.repository = repository

    def execute(self, input: ListInput) -> ListOutput[T]:
        try:
            entities, total_count = self.repository.search(
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
            return self.output(data=entities, meta=meta)

    @property
    @abstractmethod
    def output(self) -> Type[ListOutput[T]]:
        pass
