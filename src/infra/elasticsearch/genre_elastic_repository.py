from collections import defaultdict
from uuid import UUID, uuid4

from elasticsearch import Elasticsearch

from src.application.genre.list_genre import SortableFields
from src.domain.entity import Entity
from src.domain.genre.genre import Genre
from src.domain.genre.genre_repository import GenreRepository
from src.infra.elasticsearch.abstract_elastic_repository import AbstractElasticRepository
from src.infra.elasticsearch.client import GENRE_INDEX, get_elasticsearch, GENRE_CATEGORY_INDEX

GenreID = UUID
CategoryID = UUID


class GenreElasticRepository(AbstractElasticRepository, GenreRepository):
    def __init__(self, client: Elasticsearch | None = None, wait_for_refresh: bool = False):
        """
        :param client: Elasticsearch client
        :param wait_for_refresh: Wait for indexing to ensure data is available for search. Slower but consistent.
        """
        super().__init__(
            index=GENRE_INDEX,
            client=client or get_elasticsearch(),
            searchable_fields=list(SortableFields),
            wait_for_refresh=wait_for_refresh,
        )

    def save(self, entity: Entity) -> None:
        # Save related Categories
        for category_id in entity.categories:
            new_id = str(uuid4())
            self.client.index(
                index=GENRE_CATEGORY_INDEX,
                id=new_id,
                body={
                    "id": new_id,
                    "genre_id": str(entity.id),
                    "category_id": str(category_id)
                },
                refresh="wait_for" if self.wait_for_refresh else False,
            )

        # Save Genre
        entity.categories = set()
        self.client.index(
            index=self.index,
            id=str(entity.id),
            body=entity.to_dict(),
            refresh="wait_for" if self.wait_for_refresh else False,
        )

    def build_response(self, query: dict) -> tuple[list[Genre], int]:
        response = self.client.search(index=self.index, body=query)
        total_count = response["hits"]["total"]["value"]
        entities = [Genre.from_dict(hit["_source"]) for hit in response["hits"]["hits"]]

        self.enrich_with_categories(entities)

        return entities, total_count

    def enrich_with_categories(self, genres: list[Genre]) -> None:
        genre_category_map = self.fetch_genre_categories(genres)
        for genre in genres:
            genre.categories = genre_category_map.get(genre.id, set())

    def fetch_genre_categories(self, genres: list[Genre]) -> dict[GenreID, set[CategoryID]]:
        genre_ids_str = [str(genre.id) for genre in genres]

        query = {
            "query": {
                "terms": {
                    "genre_id.keyword": genre_ids_str
                }
            },
            "_source": ["genre_id", "category_id"]
        }
        response = self.client.search(index=GENRE_CATEGORY_INDEX, body=query)

        genre_category_map = defaultdict(set)
        for hit in response["hits"]["hits"]:
            genre_id = UUID(hit["_source"]["genre_id"])
            category_id = UUID(hit["_source"]["category_id"])
            genre_category_map[genre_id].add(category_id)

        return genre_category_map
