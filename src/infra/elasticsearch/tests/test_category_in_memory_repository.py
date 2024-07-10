from src.domain.factories import CategoryFactory
from src.infra.elasticsearch.category_in_memory_repository import CategoryInMemoryRepository


class TestSave:
    def test_save_add_category_if_does_not_exist(self):
        repository = CategoryInMemoryRepository()
        category = CategoryFactory(
            name="Filme",
            description="Categoria para filmes",
        )

        repository.save(category)

        assert len(repository.categories) == 1
        assert repository.categories[0] == category

    def test_save_update_category_if_already_exists(self):
        repository = CategoryInMemoryRepository()
        category = CategoryFactory(
            name="Filme",
            description="Categoria para filmes",
        )
        repository.save(category)

        category.name = "Séries"
        repository.save(category)

        assert len(repository.categories) == 1
        assert repository.categories[0] == category


class TestSearch:
    def test_search_categories(self):
        repository = CategoryInMemoryRepository()
        category = CategoryFactory(
            name="Filme",
            description="Categoria para filmes",
        )
        repository.save(category)

        categories, total_count = repository.search(search="Filme")

        assert len(categories) == 1
        assert categories[0] == category
        assert total_count == 1

    def test_search_categories_with_no_results(self):
        repository = CategoryInMemoryRepository()
        category = CategoryFactory(
            name="Filme",
            description="Categoria para filmes",
        )
        repository.save(category)

        categories, total_count = repository.search(search="Séries")

        assert len(categories) == 0
        assert total_count == 1
