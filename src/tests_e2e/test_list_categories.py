import pytest
from testcontainers.elasticsearch import ElasticSearchContainer

from src.application.category.list_category import ListCategory
from src.application.category.save_category import SaveCategory
from src.application.category.tests.factories import CategoryFactory
from src.application.listing import ListOutputMeta
from src.domain.category.category import Category
from src.infra.elasticsearch.category_elastic_repository import CategoryElasticRepository
from src.infra.elasticsearch.client import get_elasticsearch


def test_list_categories():
    client = get_elasticsearch(host="elasticsearch-test")  # from docker-compose.yml
    client.indices.delete(index="categories")
    elastic_repository = CategoryElasticRepository(client=client)

    category = CategoryFactory(name="Romance")
    print("creating category...")
    SaveCategory(repository=elastic_repository).execute(SaveCategory.Input(category))

    import ipdb; ipdb.set_trace()
    use_case = ListCategory(repository=elastic_repository)
    list_output = use_case.execute(ListCategory.Input())

    assert list_output.data[0] == category
    assert list_output.meta.total_count == 1

    # tear down elasticsearch database
    client.indices.delete(index="categories")

