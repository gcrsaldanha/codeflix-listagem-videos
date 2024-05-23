from dataclasses import asdict

from elasticsearch import Elasticsearch

from src.domain.category.category import Category
from src.domain.category.category_repository import CategoryRepository
from src.infra.elasticsearch.client import get_elasticsearch


class CategoryElasticRepository(CategoryRepository):
    def __init__(self, client: Elasticsearch | None = None):
        self.client = client or get_elasticsearch()

    def save(self, category: Category) -> None:
        self.client.index(index='categories', id=str(category.id), body=asdict(category))

    def list(self, query: str = "") -> list[Category]:
        result = self.client.search(index="categories", body={"query": {"match_all": {}}})
        return [
            Category(
                id=hit['_id'],
                name=hit['_source']['name'],
                description=hit['_source']['description'],
                is_active=hit['_source']['is_active'],
                created_at=hit['_source']['created_at'],
                updated_at=hit['_source']['updated_at'],
            ) for hit in result['hits']['hits']
        ]
