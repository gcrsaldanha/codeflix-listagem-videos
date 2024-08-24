from abc import ABC, abstractmethod

from elasticsearch import Elasticsearch

from src.application.listing import SortDirection
from src.config import DEFAULT_PAGINATION_SIZE
from src.domain.entity import Entity
from src.domain.repository import Repository


class AbstractElasticRepository(Repository):
    def __init__(
        self,
        index: str,
        client: Elasticsearch,
        searchable_fields: list[str],
        wait_for_refresh: bool,
    ):
        self.index = index
        self.client = client
        self.wait_for_refresh = wait_for_refresh
        self.searchable_fields = searchable_fields

    def save(self, entity: Entity) -> None:
        self.client.index(
            index=self.index,
            id=str(entity.id),
            body=entity.to_dict(),
            refresh="wait_for" if self.wait_for_refresh else False,
        )

    def search(
        self,
        page: int = 1,
        per_page: int = DEFAULT_PAGINATION_SIZE,
        search: str | None = None,
        sort: str | None = None,
        direction: SortDirection = SortDirection.ASC,
    ) -> tuple[list[Entity], int]:
        if self.is_empty():
            return [], 0

        query = self.build_query(direction, page, per_page, search, sort)
        return self.build_response(query)

    @abstractmethod
    def build_response(self, query: dict) -> tuple[list[Entity], int]:
        raise NotImplementedError

    def build_query(
        self,
        direction: SortDirection,
        page: int,
        per_page: int,
        search: str | None,
        sort: str | None,
    ) -> dict:
        query = {
            "query": {
                "bool": {
                    "must": (
                        [{"multi_match": {"query": search, "fields": self.searchable_fields}}]
                        if search
                        else {"match_all": {}}
                    )
                }
            },
            "from": (page - 1) * per_page,
            "size": per_page,
            "sort": [{f"{sort}.keyword": {"order": direction}}] if sort else [],  # Use .keyword for exact match
        }
        return query

    def is_empty(self) -> bool:
        return (
            not self.client.indices.exists(index=self.index)
            or self.client.count(index=self.index, body={"query": {"match_all": {}}})["count"] == 0
        )
