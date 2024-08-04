from collections import defaultdict

from elasticsearch import Elasticsearch

from src.application.genre.list_genre import SortableFields
from src.application.listing import SortDirection
from src.config import DEFAULT_PAGINATION_SIZE
from src.domain.genre.genre import Genre
from src.domain.genre.genre_repository import GenreRepository
from src.infra.elasticsearch.client import get_elasticsearch, GENRE_INDEX, GENRE_CATEGORY_INDEX


class GenreElasticRepository(GenreRepository):
    # TODO: abstract this repository to a base class
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
        # Elasticsearch cannot serialize set objects, so we need to convert it to a list
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
    ) -> tuple[list[Genre], int]:
        if self.is_empty():
            return [], 0

        query = self.build_query(direction, page, per_page, search, sort)
        return self.build_response(query)

    def fetch_all_genres(self) -> list[dict]:
        query = {
            "query": {
                "match_all": {}
            }
        }
        response = self.client.search(index=self.index, body=query)
        return response["hits"]["hits"]

    def fetch_all_genre_category_associations(self) -> dict[str, set[str]]:
        query = {
            "query": {
                "match_all": {}
            },
            "_source": ["genre_id", "category_id"]
        }
        response = self.client.search(index=GENRE_CATEGORY_INDEX, body=query)

        genre_category_map = defaultdict(set)
        for hit in response["hits"]["hits"]:
            genre_id = hit["_source"]["genre_id"]
            category_id = hit["_source"]["category_id"]
            genre_category_map[genre_id].add(category_id)

        return genre_category_map

    def build_response(self, query: dict) -> tuple[list[Genre], int]:
        # Fetch all genres
        genre_hits = self.fetch_all_genres()

        # Fetch all genre-category associations
        genre_category_map = self.fetch_all_genre_category_associations()

        genres = []
        for genre_hit in genre_hits:
            genre_dict = genre_hit["_source"]
            genre_dict["categories"] = genre_category_map.get(genre_dict["id"], set())
            genres.append(Genre.from_dict(genre_dict))

        total_count = len(genres)
        return genres, total_count

    def build_query(self, direction, page, per_page, search, sort):
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
            "sort": [{f"{sort}.keyword": {"order": direction}}] if sort else [],
        }
        return query

    def is_empty(self) -> bool:
        return (
                not self.client.indices.exists(index=self.index)
                or self.client.count(index=self.index, body={"query": {"match_all": {}}})["count"] == 0
        )
