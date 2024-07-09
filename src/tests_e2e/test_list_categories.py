import time
from typing import Generator, Iterator
from elasticsearch import Elasticsearch
import pytest
from testcontainers.elasticsearch import ElasticSearchContainer

from src.application.category.list_category import ListCategory
from src.application.category.save_category import SaveCategory
from src.application.category.tests.factories import CategoryFactory
from src.application.listing import ListOutputMeta
from src.domain.category.category import Category
from src.infra.elasticsearch.category_elastic_repository import CategoryElasticRepository
from src.infra.elasticsearch.client import INDEXES, get_elasticsearch

ELASTICSEARCH_HOST = "elasticsearch-test"  # from docker-compose.yml
# ELASTICSEARCH_HOST = "localhost"  # if running tests from host machine


def setup_elasticsearch():
    es = get_elasticsearch(host=ELASTICSEARCH_HOST)
    for index in INDEXES:
        es.indices.create(index=index) if not es.indices.exists(index=index) else None


def teardown_elasticsearch():
    es = get_elasticsearch(host=ELASTICSEARCH_HOST)
    for index in INDEXES:
        es.indices.delete(index=index)


@pytest.fixture
def elasticsearch() -> Iterator[Elasticsearch]:
    setup_elasticsearch()
    yield get_elasticsearch(host=ELASTICSEARCH_HOST)
    teardown_elasticsearch()


def test_list_categories_with_pagination(elasticsearch: Elasticsearch):
    # TODO: Desafio: simular eventos Kafka
    elastic_repository = CategoryElasticRepository(client=elasticsearch, wait_for_refresh=True)

    romance = CategoryFactory(name="Romance")
    drama = CategoryFactory(name="Drama")
    short = CategoryFactory(name="Short")

    SaveCategory(repository=elastic_repository).execute(SaveCategory.Input(romance))
    SaveCategory(repository=elastic_repository).execute(SaveCategory.Input(drama))
    SaveCategory(repository=elastic_repository).execute(SaveCategory.Input(short))

    use_case = ListCategory(repository=elastic_repository)
    list_output = use_case.execute(ListCategory.Input(page=1, per_page=2))

    assert list_output == ListCategory.Output(
        data=[drama, romance],  # Sorted by name
        meta=ListOutputMeta(page=1, per_page=2, total_count=3),
    )
    assert list_output.meta.next_page == 2

    list_output = use_case.execute(ListCategory.Input(page=2, per_page=2))
    assert list_output == ListCategory.Output(
        data=[short],
        meta=ListOutputMeta(page=2, per_page=2, total_count=3),
    )
    assert list_output.meta.next_page is None
