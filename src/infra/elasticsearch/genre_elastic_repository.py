from typing import List, Tuple

from elasticsearch import Elasticsearch

from src.application.genre.list_genre import SortableFields
from src.application.listing import SortDirection
from src.config import DEFAULT_PAGINATION_SIZE
from src.domain.category.category import Category
from src.domain.category.category_repository import CategoryRepository
from src.domain.genre.genre import Genre
from src.domain.genre.genre_repository import GenreRepository
from src.infra.elasticsearch.client import CATEGORY_INDEX, get_elasticsearch, GENRE_INDEX


class GenreElasticRepository(GenreRepository):
    def __init__(self, client: Elasticsearch | None = None, wait_for_refresh: bool = False):
        """
        :param client: Elasticsearch client
        :param wait_for_refresh: Wait for indexing to ensure data is available for search. Slower but consistent.
        """
        self.index = GENRE_INDEX
        self.searchable_fields = list(SortableFields)
        self.client = client or get_elasticsearch()
        self.wait_for_refresh = wait_for_refresh

    def save(self, entity: Genre) -> None:
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
    ) -> Tuple[List[Genre], int]:
        if (
            not self.client.indices.exists(index=self.index)
            or self.client.count(index=self.index, body={"query": {"match_all": {}}})["count"] == 0
        ):
            return [], 0

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
            "sort": [{f"{sort}.keyword": {"order": direction}}] if sort else [],  # Use .keyword for efficient sorting
        }

        response = self.client.search(index=self.index, body=query)
        total_count = response["hits"]["total"]["value"]
        genres = [Genre.from_dict(hit["_source"]) for hit in response["hits"]["hits"]]

        return genres, total_count
