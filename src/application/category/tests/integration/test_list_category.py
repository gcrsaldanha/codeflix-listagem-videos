import pytest

from src.application.category.list_category import ListCategory
from src.application.category.tests.factories import CategoryFactory
from src.application.listing import ListOutputMeta
from src.domain.category.category import Category
from src.infra.elasticsearch.in_memory_category_repository import InMemoryCategoryRepository


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
        response = use_case.execute(
            input=ListCategory.Input(
                per_page=2,
            )
        )

        expected_output = ListCategory.Output(
            data=[
                category_documentary,
                category_movie,
            ],
            meta=ListOutputMeta(
                page=1,
                per_page=2,
                next_page=None,
                total_count=3,
            ),
        )

        assert response == expected_output
