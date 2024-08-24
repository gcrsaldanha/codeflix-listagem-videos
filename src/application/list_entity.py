from abc import ABC, abstractmethod
from typing import Type

from src.application.exceptions import SearchError
from src.application.listing import ListInput, ListOutput, ListOutputMeta
from src.domain.repository import Repository


class ListEntity(ABC):
    def __init__(self, repository: Repository) -> None:
        self.repository = repository

    def execute(self, input: ListInput) -> ListOutput:
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
            return ListOutput(data=entities, meta=meta)
