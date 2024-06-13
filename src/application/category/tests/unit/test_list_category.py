from unittest.mock import create_autospec

import pytest

from src.application.category.list_category import ListCategory
from src.application.category.tests.factories import CategoryFactory
from src.application.listing import ListOutputMeta
from src.domain.category.category import Category
from src.domain.category.category_repository import CategoryRepository


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
        repository.list.return_value = []
        return repository

    @pytest.fixture
    def mock_populated_repository(
        self,
        category_movie: Category,
        category_series: Category,
        category_documentary: Category,
    ) -> CategoryRepository:
        repository = create_autospec(CategoryRepository)
        repository.list.return_value = [
            category_movie,
            category_series,
            category_documentary,  # Fora de "ordem" - Application que ordena
        ]
        return repository

    def test_when_no_categories_then_return_empty_list(
        self,
        mock_empty_repository: CategoryRepository,
    ) -> None:
        use_case = ListCategory(repository=mock_empty_repository)
        response = use_case.execute(input=ListCategory.Input())

        assert response == ListCategory.Output(
            data=[],
            meta=ListOutputMeta(
                page=1,
                per_page=2,
                total=0,
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

        assert response == ListCategory.Output(
            data=[
                ListCategory.CategoryOutput(
                    id=category_documentary.id,
                    name=category_documentary.name,
                    description=category_documentary.description,
                    is_active=category_documentary.is_active,
                    created_at=category_documentary.created_at,
                    updated_at=category_documentary.updated_at,
                ),
                ListCategory.CategoryOutput(
                    id=category_movie.id,
                    name=category_movie.name,
                    description=category_movie.description,
                    is_active=category_movie.is_active,
                    created_at=category_movie.created_at,
                    updated_at=category_movie.updated_at,
                ),
                # Documentary vem antes, "empurra" o Movie para fora da página
                # Por isso precisamos ordernar a lista de categorias antes de paginar
                # ListCategory.CategoryOutput(
                #     id=category_series.id,
                #     name=category_series.name,
                #     description=category_series.description,
                #     is_active=category_series.is_active,
                # ),
            ],
            meta=ListOutputMeta(
                page=1,
                per_page=2,
                total=3,
            ),
        )

    def test_fetch_page_without_elements(self, mock_populated_repository: CategoryRepository) -> None:
        use_case = ListCategory(repository=mock_populated_repository)
        response = use_case.execute(input=ListCategory.Input(page=3))

        assert response == ListCategory.Output(
            data=[],
            meta=ListOutputMeta(
                page=3,
                per_page=2,
                total=3,
            ),
        )

    def test_fetch_last_page_with_elements(
        self,
        mock_populated_repository: CategoryRepository,
        category_series: Category,  # Foi "empurrado" para última página
    ) -> None:
        use_case = ListCategory(repository=mock_populated_repository)
        response = use_case.execute(input=ListCategory.Input(page=2))

        assert response == ListCategory.Output(
            data=[
                ListCategory.CategoryOutput(
                    id=category_series.id,
                    name=category_series.name,
                    description=category_series.description,
                    is_active=category_series.is_active,
                    created_at=category_series.created_at,
                    updated_at=category_series.updated_at,
                )
            ],
            meta=ListOutputMeta(
                page=2,
                per_page=2,
                total=3,
            ),
        )
