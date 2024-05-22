from uuid import UUID
from src.core.category.use_cases.save_category import SaveCategory
from src.core.category.infra.in_memory_category_repository import InMemoryCategoryRepository


class TestSaveCategory:
    def test_save_category_with_valid_data(self):
        repository = InMemoryCategoryRepository()  # SQLAlchmmy / DjangoORMRepository
        use_case = SaveCategory(repository=repository)
        request = SaveCategory.Input(
            name="Filme",
            description="Categoria para filmes",
            is_active=True,  # default
        )

        response = use_case.execute(request)

        assert response is not None
        assert isinstance(response.id, UUID)
        assert len(repository.categories) == 1

        persisted_category = repository.categories[0]
        assert persisted_category.id == response.id
        assert persisted_category.name == "Filme"
        assert persisted_category.description == "Categoria para filmes"
        assert persisted_category.is_active is True

    def test_save_inactive_category_with_valid_data(self):
        repository = InMemoryCategoryRepository()
        use_case = SaveCategory(repository=repository)
        request = SaveCategory.Input(
            name="Filme",
            description="Categoria para filmes",
            is_active=False,
        )

        response = use_case.execute(request)
        persisted_category = repository.categories[0]

        assert persisted_category.id == response.id
        assert persisted_category.name == "Filme"
        assert persisted_category.description == "Categoria para filmes"
        assert persisted_category.is_active == False
