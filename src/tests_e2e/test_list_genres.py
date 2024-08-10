from typing import Iterator

import pytest
from elasticsearch import Elasticsearch
from fastapi.testclient import TestClient

from src.application.genre.list_genre import ListGenre
from src.application.listing import ListOutputMeta
from src.config import ELASTICSEARCH_TEST_HOST
from src.domain.factories import CategoryFactory, GenreFactory
from src.infra.api.http.genre_router import get_repository
from src.infra.api.http.main import app
from src.infra.repository.elastic.client import get_elasticsearch, INDEXES
from src.infra.repository.elastic.genre_elastic_repository import GenreElasticRepository


@pytest.fixture
def elasticsearch() -> Iterator[Elasticsearch]:
    es = get_elasticsearch(host=ELASTICSEARCH_TEST_HOST)

    for index in INDEXES:
        es.indices.create(index=index) if not es.indices.exists(index=index) else None

    yield es

    for index in INDEXES:
        es.indices.delete(index=index)


@pytest.fixture
def test_repository(elasticsearch) -> Iterator[GenreElasticRepository]:
    yield GenreElasticRepository(client=elasticsearch, wait_for_refresh=True)


@pytest.fixture
def test_client(test_repository) -> Iterator[TestClient]:
    app.dependency_overrides[get_repository] = lambda: test_repository
    yield TestClient(app)
    app.dependency_overrides.clear()


def test_list_genres_with_pagination(
    test_repository: GenreElasticRepository,
    test_client: TestClient,
    elasticsearch: Elasticsearch,
):
    film = CategoryFactory(name="Film")
    short = CategoryFactory(name="Short")

    drama = GenreFactory(name="Drama", categories=set())
    romance = GenreFactory(name="Romance", categories=set())
    comedy = GenreFactory(name="Comedy", categories=set())

    test_repository.save(drama)
    test_repository.save(romance)
    test_repository.save(comedy)

    use_case = ListGenre(repository=test_repository)
    list_output = use_case.execute(ListGenre.Input(page=1, per_page=2))

    assert list_output == ListGenre.Output(
        data=[comedy, drama],
        meta=ListOutputMeta(page=1, per_page=2, total_count=3),
    )
    assert list_output.meta.next_page == 2

    # Fetch next page
    list_output = use_case.execute(ListGenre.Input(page=2, per_page=2))
    assert list_output == ListGenre.Output(
        data=[romance],
        meta=ListOutputMeta(page=2, per_page=2, total_count=3),
    )
    assert list_output.meta.next_page is None

    # Fetch using HTTP
    response = test_client.get("/genres?page=1&per_page=2")
    assert response.status_code == 200
    data = response.json()["data"]
    meta = response.json()["meta"]

    assert len(data) == 2
    assert data[0]["name"] == "Comedy"
    assert data[0]["id"] == f"{comedy.id}"
    assert data[0]["categories"] == []
    assert data[0]["is_active"] is True

    assert data[1]["name"] == "Drama"
    assert data[1]["id"] == f"{drama.id}"
    assert data[1]["categories"] == [str(film.id)]
    assert data[1]["is_active"] is True

    assert meta == {
        "page": 1,
        "per_page": 2,
        "total_count": 3,
        "next_page": 2,
    }
