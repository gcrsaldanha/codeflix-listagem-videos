import pytest

from src.application.category.list_category import ListCategory
from src.application.listing import ListOutputMeta
from src.domain.category.category import Category
from src.infra.category.in_memory_category_repository import (
    InMemoryCategoryRepository,
)


class TestListCategory:
    @pytest.fixture
    def category_movie(self) -> Category:
        return Category(
            name="Filme",
            description="Categoria de filmes",
        )

    @pytest.fixture
    def category_series(self) -> Category:
        return Category(
            name="Séries",
            description="Categoria de séries",
        )

    @pytest.fixture
    def category_documentary(self) -> Category:
        return Category(
            name="Documentário",
            description="Categoria de documentários",
        )

    def test_when_no_categories_then_return_empty_list(self) -> None:
        empty_repository = InMemoryCategoryRepository()
        use_case = ListCategory(repository=empty_repository)
        response = use_case.execute(input=ListCategory.Input())

        assert response == ListCategory.Output(
            data=[],
            meta=ListOutputMeta(),
        )

    def test_when_categories_exist_then_return_mapped_list(
        self,
        category_movie: Category,
        category_series: Category,
        category_documentary: Category,
    ) -> None:
        repository = InMemoryCategoryRepository()
        repository.save(category=category_movie)
        repository.save(category=category_series)
        repository.save(category=category_documentary)

        use_case = ListCategory(repository=repository)
        response = use_case.execute(input=ListCategory.Input())

        assert response == ListCategory.Output(
            data=[
                ListCategory.CategoryOutput(
                    id=category_documentary.id,
                    name=category_documentary.name,
                    description=category_documentary.description,
                    is_active=category_documentary.is_active,
                ),
                ListCategory.CategoryOutput(
                    id=category_movie.id,
                    name=category_movie.name,
                    description=category_movie.description,
                    is_active=category_movie.is_active,
                ),
                # "Empurrado" por category_documentary
                # ListCategory.CategoryOutput(
                #     id=category_series.id,
                #     name=category_series.name,
                #     description=category_series.description,
                #     is_active=category_series.is_active,
                # ),
            ],
            meta=ListOutputMeta(
                current_page=1,
                per_page=2,
                total=3,
            ),
        )
