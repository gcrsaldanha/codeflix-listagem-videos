from unittest.mock import create_autospec

import pytest

from src.application.category.list_category import ListCategory, SortableFields
from src.application.genre.list_genre import ListGenre
from src.domain.factories import CategoryFactory
from src.application.listing import ListOutputMeta, SortDirection, ListOutput
from src.domain.category.category import Category
from src.domain.category.category_repository import CategoryRepository
from src import config


class TestListCategory:
    @pytest.fixture
    def category_movie(self) -> Category:
        return CategoryFactory(
            name="Filme",
            description="Categoria de filmes",
        )

    @pytest.fixture
    def category_series(self) -> Category:
        return CategoryFactory(
            name="Séries",
            description="Categoria de séries",
        )

    @pytest.fixture
    def category_documentary(self) -> Category:
        return CategoryFactory(
            name="Documentário",
            description="Categoria de documentários",
        )

    @pytest.fixture
    def mock_empty_repository(self) -> CategoryRepository:
        repository = create_autospec(CategoryRepository)
        repository.search.return_value = ([], 0)
        return repository

    @pytest.fixture
    def mock_populated_repository(
        self,
        category_movie: Category,
        category_series: Category,
        category_documentary: Category,
    ) -> CategoryRepository:
        repository = create_autospec(CategoryRepository)
        repository.search.return_value = (
            [
                category_documentary,
                category_movie,
                category_series,
            ],
            3,
        )
        return repository

    def test_when_no_categories_then_return_empty_list(
        self,
        mock_empty_repository: CategoryRepository,
    ) -> None:
        use_case = ListCategory(repository=mock_empty_repository)
        response = use_case.execute(input=ListCategory.Input())

        assert response == ListOutput(
            data=[],
            meta=ListOutputMeta(
                page=1,
                per_page=config.DEFAULT_PAGINATION_SIZE,
                total_count=0,
            ),
        )

    def test_when_categories_exist_then_return_mapped_list(
        self,
        mock_populated_repository: CategoryRepository,
        category_movie: Category,
        category_series: Category,
        category_documentary: Category,
    ) -> None:
        use_case = ListCategory(repository=mock_populated_repository)
        response = use_case.execute(input=ListCategory.Input())

        assert response == ListOutput(
            data=[
                category_documentary,
                category_movie,
                category_series,
            ],
            meta=ListOutputMeta(
                page=1,
                per_page=config.DEFAULT_PAGINATION_SIZE,
                total_count=3,
            ),
        )

        mock_populated_repository.search.assert_called_once_with(
            page=1,
            per_page=5,
            sort=SortableFields.NAME,
            direction=SortDirection.ASC,
            search=None,
        )
