from datetime import datetime
from fastapi.testclient import TestClient

from src.config import ELASTICSEARCH_TEST_HOST
from src.infra.api.http.category_router import get_repository
from src.infra.api.http.main import app
from typing import Iterator
from elasticsearch import Elasticsearch
import pytest

from src.application.category.list_category import ListCategory
from src.domain.factories import CategoryFactory
from src.application.listing import ListOutputMeta, ListOutput
from src.infra.elasticsearch.category_elastic_repository import CategoryElasticRepository
from src.infra.elasticsearch.client import get_elasticsearch, INDEXES


@pytest.fixture
def elasticsearch() -> Iterator[Elasticsearch]:
    es = get_elasticsearch(host=ELASTICSEARCH_TEST_HOST)

    for index in INDEXES:
        es.indices.create(index=index) if not es.indices.exists(index=index) else None

    yield es

    for index in INDEXES:
        es.indices.delete(index=index)


@pytest.fixture
def test_repository(elasticsearch) -> Iterator[CategoryElasticRepository]:
    yield CategoryElasticRepository(client=elasticsearch, wait_for_refresh=True)


@pytest.fixture
def test_client(test_repository) -> Iterator[TestClient]:
    app.dependency_overrides[get_repository] = lambda: test_repository
    yield TestClient(app)
    app.dependency_overrides.clear()


def test_list_categories_with_pagination(
    test_repository: CategoryElasticRepository,
    test_client: TestClient,
    elasticsearch: Elasticsearch,
):
    romance = CategoryFactory(name="Romance")
    drama = CategoryFactory(name="Drama")
    short = CategoryFactory(name="Short")

    test_repository.save(romance)
    test_repository.save(drama)
    test_repository.save(short)

    use_case = ListCategory(repository=test_repository)
    list_output = use_case.execute(ListCategory.Input(page=1, per_page=2))

    assert list_output == ListOutput(
        data=[drama, romance],  # Sorted by name
        meta=ListOutputMeta(page=1, per_page=2, total_count=3),
    )
    assert list_output.meta.next_page == 2

    list_output = use_case.execute(ListCategory.Input(page=2, per_page=2))
    assert list_output == ListOutput(
        data=[short],
        meta=ListOutputMeta(page=2, per_page=2, total_count=3),
    )
    assert list_output.meta.next_page is None

    response = test_client.get("/categories?page=1&per_page=2")
    assert response.status_code == 200
    data = response.json()["data"]
    meta = response.json()["meta"]

    assert data[0]["name"] == "Drama"
    assert data[0]["description"] == drama.description
    assert data[0]["id"] == f"{drama.id}"
    assert data[0]["is_active"] is True
    # serialization of datetime uses "Z" instead of "00:00", we could also manually set the datetime
    assert datetime.fromisoformat(response.json()["data"][0]["created_at"]) == drama.created_at
    assert datetime.fromisoformat(response.json()["data"][0]["updated_at"]) == drama.updated_at

    # Sorted by name
    assert data[1]["name"] == "Romance"
    assert data[1]["description"] == romance.description

    assert meta["page"] == 1
    assert meta["per_page"] == 2
    assert meta["total_count"] == 3
    assert meta["next_page"] == 2
