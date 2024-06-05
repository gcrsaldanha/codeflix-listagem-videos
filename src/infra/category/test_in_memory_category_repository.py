from src.application.category.tests.factories import CategoryFactory
from src.infra.category.in_memory_category_repository import InMemoryCategoryRepository


class TestSave:
    def test_can_save_category(self):
        repository = InMemoryCategoryRepository()
        category = CategoryFactory(
            name="Filme",
            description="Categoria para filmes",
        )

        repository.save(category)

        assert len(repository.categories) == 1
        assert repository.categories[0] == category
