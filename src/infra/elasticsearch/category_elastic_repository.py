from elasticsearch import Elasticsearch

from src.application.category.list_category import SortableFields
from src.domain.category.category import Category
from src.domain.category.category_repository import CategoryRepository
from src.infra.elasticsearch.abstract_elastic_repository import AbstractElasticRepository
from src.infra.elasticsearch.client import CATEGORY_INDEX, get_elasticsearch


class CategoryElasticRepository(AbstractElasticRepository, CategoryRepository):
    def __init__(
        self,
        client: Elasticsearch | None = None,
        wait_for_refresh: bool = True,
    ) -> None:
        """
        :param wait_for_refresh: Wait for indexing to ensure data is available for search. Slower but consistent.
        """
        super().__init__(
            index=CATEGORY_INDEX,
            client=client or get_elasticsearch(),
            searchable_fields=list(SortableFields),
            wait_for_refresh=wait_for_refresh,
        )

    def build_response(self, query: dict) -> tuple[list[Category], int]:
        response = self.client.search(index=self.index, body=query)
        total_count = response["hits"]["total"]["value"]
        entities = [Category.from_dict(hit["_source"]) for hit in response["hits"]["hits"]]

        return entities, total_count
