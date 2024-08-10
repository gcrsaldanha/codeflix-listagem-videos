from collections import defaultdict
from uuid import UUID

from elasticsearch import Elasticsearch

from src.application.genre.list_genre import SortableFields
from src.domain.entity import Entity
from src.domain.genre.genre import Genre
from src.domain.genre.genre_repository import GenreRepository
from src.infra.repository.elastic.abstract_elastic_repository import AbstractElasticRepository
from src.infra.repository.elastic.client import GENRE_INDEX, get_elasticsearch, GENRE_CATEGORY_INDEX

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

    def build_response(self, query: dict) -> tuple[list[Genre], int]:
        response = self.client.search(index=self.index, body=query)
        total_count = response["hits"]["total"]["value"]
        entities = [Genre.from_dict(hit["_source"]) for hit in response["hits"]["hits"]]

        self.enrich_with_categories(entities)

        return entities, total_count

    def enrich_with_categories(self, genres: list[Genre]) -> None:
        genre_category_map = self.fetch_genre_categories(genres)
        for genre in genres:
            genre.set_categories(genre_category_map.get(genre.id, set()))

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


# client = get_elasticsearch()
# query = {
#     "query": {
#         "terms": {
#             "genre_id": ["51cae8cd-5208-11ef-a09a-0242ac120003"]
#         }
#     },
#     "_source": ["genre_id", "category_id"]
# }
#
# response = client.search(index=GENRE_CATEGORY_INDEX, body=query)


# query_exact = {
#     "query": {
#         "term": {
#             "id": "51cae8cd-5208-11ef-a09a-0242ac120003"
#         }
#     },
# }
#
#
# curl -X GET "localhost:9200/catalog-db.codeflix.categories/_search?pretty&pretty" -H 'Content-Type: application/json' -d'
# {
#   "query": {
#     "terms": {
#         "color" : {
#             "index" : "my-index-000001",
#             "id" : "2",
#             "path" : "color"
#         }
#     }
#   }
# }
# '
#
#
# curl -X GET "localhost:9200/_search?pretty" -H 'Content-Type: application/json' -d'
# {
#   "query": {
#     "terms": {
#       "name": ["Romance", "Drama"],
#     }
#   }
# }
# '
#
#
# curl -X GET "localhost:9200/_search?pretty" -H 'Content-Type: application/json' -d'
# {
#   "query": {
#     "terms": {
#       "name": ["Filme"]
#     }
#   }
# }
# '
