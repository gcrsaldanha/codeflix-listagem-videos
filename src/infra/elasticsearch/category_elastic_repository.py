from typing import List, Literal, Tuple

from elasticsearch import Elasticsearch

from src.application.listing import SortDirection
from src.config import DEFAULT_PAGINATION_SIZE
from src.domain.category.category import Category
from src.domain.category.category_repository import CategoryRepository
from src.infra.elasticsearch.client import CATEGORY_INDEX, get_elasticsearch


class CategoryElasticRepository(CategoryRepository):
    def __init__(self, client: Elasticsearch = None, wait_for_refresh: bool = False):
        """
        :param client: Elasticsearch client
        :param wait_for_refresh: Wait for indexing to ensure data is available for search. Slower but consistent.
        """
        self.index = CATEGORY_INDEX
        self.searchable_fields = ["name", "description"]
        self.client = client or get_elasticsearch()
        self.wait_for_refresh = wait_for_refresh

        if not self.client.indices.exists(index=self.index):
            self.client.indices.create(index=self.index)

    def save(self, category: Category) -> None:
        self.client.index(
            index=self.index,
            id=str(category.id),
            body=self.from_domain(category),
            refresh="wait_for" if self.wait_for_refresh else False,
        )

    def search(
        self,
        page: int = 1,
        per_page: int = DEFAULT_PAGINATION_SIZE,
        search: str | None = None,
        sort: str | None = None,
        direction: SortDirection = SortDirection.ASC,
    ) -> Tuple[List[Category], int]:
        if (
            not self.client.indices.exists(index=self.index)
            or self.client.count(index=self.index, body={"query": {"match_all": {}}})["count"] == 0
        ):
            return [], 0

        if sort in self.searchable_fields:
            sort_field = f"{sort}.keyword"  # Search for exact match rather than analyzed text
        else:
            sort_field = sort

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
            "sort": [{sort_field: {"order": direction}}] if sort else [],
        }

        response = self.client.search(index=self.index, body=query)
        total_count = response["hits"]["total"]["value"]
        categories = [self.to_domain(hit["_source"]) for hit in response["hits"]["hits"]]

        return categories, total_count


"""
response = {
    "took": 68,
    "timed_out": False,
    "_shards": {"total": 1, "successful": 1, "skipped": 0, "failed": 0},
    "hits": {
        "total": {"value": 5, "relation": "eq"},
        "max_score": 1.0,
        "hits": [
            {
                "_index": "categories",
                "_id": "123e4567-e89b-12d3-a456-426614174000",
                "_score": 1.0,
                "_source": {
                    "id": "123e4567-e89b-12d3-a456-426614174000",
                    "name": "Category Name",
                    "description": "Category Description",
                    "is_active": True,
                    "created_at": "2023-01-01T00:00:00",
                    "updated_at": "2023-01-01T00:00:00",
                },
            },
            {
                "_index": "categories",
                "_id": "124e4567-e89b-12d3-a456-426614174000",
                "_score": 1.0,
                "_source": {
                    "id": "124e4567-e89b-12d3-a456-426614174000",
                    "name": "Category Name",
                    "description": "Category Description",
                    "is_active": True,
                    "created_at": "2023-01-01T00:00:00",
                    "updated_at": "2023-01-01T00:00:00",
                },
            },
            {
                "_index": "categories",
                "_id": "2057b909-b100-422d-9b8f-a1fc183a791b",
                "_score": 1.0,
                "_source": {
                    "id": "2057b909-b100-422d-9b8f-a1fc183a791b",
                    "created_at": "2024-05-23T11:56:11.111340",
                    "updated_at": "2024-05-23T11:56:11.112528",
                    "notification": {},
                    "name": "Nova Category",
                    "description": "",
                    "is_active": True,
                },
            },
            {
                "_index": "categories",
                "_id": "71f4bf9f-c6d0-4f47-bb48-c1e0f3c93c58",
                "_score": 1.0,
                "_source": {
                    "id": "71f4bf9f-c6d0-4f47-bb48-c1e0f3c93c58",
                    "created_at": "2024-05-23T13:34:55.686050",
                    "updated_at": "2024-05-23T13:34:55.686232",
                    "notification": {},
                    "name": "Categoria X",
                    "description": "",
                    "is_active": True,
                },
            },
            {
                "_index": "categories",
                "_id": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
                "_score": 1.0,
                "_source": {
                    "id": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
                    "name": "string",
                    "description": "string",
                    "is_active": True,
                    "created_at": "2024-06-06T10:05:40.822000+00:00",
                    "updated_at": "2024-06-06T10:05:40.822000+00:00",
                },
            },
        ],
    },
}
"""
