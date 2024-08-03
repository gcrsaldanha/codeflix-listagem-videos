from elasticsearch import Elasticsearch

from src.application.category.list_category import SortableFields
from src.application.listing import SortDirection
from src.config import DEFAULT_PAGINATION_SIZE
from src.domain.category.category import Category
from src.domain.category.category_repository import CategoryRepository
from src.infra.elasticsearch.client import CATEGORY_INDEX, get_elasticsearch


class CategoryElasticRepository(CategoryRepository):
    def __init__(self, client: Elasticsearch | None = None, wait_for_refresh: bool = False):
        """
        :param client: Elasticsearch client
        :param wait_for_refresh: Wait for indexing to ensure data is available for search. Slower but consistent.
        """
        self.index = CATEGORY_INDEX
        self.searchable_fields = list(SortableFields)
        self.client = client or get_elasticsearch()
        self.wait_for_refresh = wait_for_refresh

    def save(self, entity: Category) -> None:
        # TODO: not used?
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
    ) -> tuple[list[Category], int]:
        if self.is_empty():
            return [], 0

        query = self.build_query(direction, page, per_page, search, sort)
        return self.build_response(query)

    def build_response(self, query: dict) -> tuple[list[Category], int]:
        response = self.client.search(index=self.index, body=query)
        total_count = response["hits"]["total"]["value"]

        categories = []
        for hit in response["hits"]["hits"]:
            category_dict = hit["_source"]
            category_dict["id"] = category_dict.pop("external_id")
            categories.append(Category.from_dict(category_dict))

        return categories, total_count

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
            "sort": [{f"{sort}.keyword": {"order": direction}}] if sort else [],  # Use .keyword for efficient sorting
        }
        return query

    def is_empty(self) -> bool:
        return (
            not self.client.indices.exists(index=self.index)
            or self.client.count(index=self.index, body={"query": {"match_all": {}}})["count"] == 0
        )
