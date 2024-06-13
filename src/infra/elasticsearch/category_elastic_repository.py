from typing import List, Tuple

from elasticsearch import Elasticsearch

from src.domain.category.category import Category
from src.infra.elasticsearch.client import get_elasticsearch

from src.domain.category.category_repository import CategoryRepository


class CategoryElasticRepository(CategoryRepository):
    def __init__(self, client: Elasticsearch = None):
        self.client = client or get_elasticsearch()

    def save(self, category: Category) -> None:
        self.client.index(index="categories", id=str(category.id), body=self.from_domain(category))

    def list(self, query: str = "") -> List[Category]:
        result = self.client.search(index="categories", body={"query": {"match_all": {}}})
        return [self.to_domain(hit["_source"]) for hit in result["hits"]["hits"]]

    def search(
        self, search: str = None, page: int = 1, per_page: int = 10, sort: str = None, direction: str = "asc"
    ) -> Tuple[List[Category], int, int]:
        if sort in {"name", "description"}:
            sort_field = f"{sort}.keyword"
        else:
            sort_field = sort

        query = {
            "query": {
                "bool": {
                    "must": (
                        [{"multi_match": {"query": search, "fields": ["name", "description"]}}]
                        if search
                        else {"match_all": {}}
                    )
                }
            },
            "from": (page - 1) * per_page,
            "size": per_page,
            "sort": [{sort_field: {"order": direction}}] if sort else [],
        }

        response = self.client.search(index="categories", body=query)
        total_count = response["hits"]["total"]["value"]
        categories = [self.to_domain(hit["_source"]) for hit in response["hits"]["hits"]]

        return categories, total_count

    def to_domain(self, data: dict) -> Category:
        return Category(
            id=data["id"],
            name=data["name"],
            description=data["description"],
            is_active=data["is_active"],
            created_at=data["created_at"],
            updated_at=data["updated_at"],
        )

    def from_domain(self, category: Category) -> dict:
        return {
            "id": category.id,
            "name": category.name,
            "description": category.description,
            "is_active": category.is_active,
            "created_at": category.created_at,
            "updated_at": category.updated_at,
        }


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
