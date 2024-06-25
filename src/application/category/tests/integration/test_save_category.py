import uuid
from datetime import datetime, timezone
from uuid import UUID

from src.application.category.save_category import SaveCategory
from src.domain.category.category import Category
from src.infra.tests.in_memory_category_repository import InMemoryCategoryRepository


class TestSaveCategory:
    def test_when_category_does_not_exist_then_create_it(self):
        repository = InMemoryCategoryRepository()
        use_case = SaveCategory(repository=repository)
        id = uuid.uuid4()
        now = datetime.now(timezone.utc)
        request = SaveCategory.Input(
            Category(
                id=id,
                name="Filme",
                description="Categoria para filmes",
                is_active=True,
                created_at=now,
                updated_at=now,
            )
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
        id = uuid.uuid4()
        now = datetime.now(timezone.utc)
        request = SaveCategory.Input(
            Category(
                id=id,
                name="Filme",
                description="Categoria para filmes",
                is_active=False,
                created_at=now,
                updated_at=now,
            ),
        )

        response = use_case.execute(request)
        persisted_category = repository.categories[0]

        assert persisted_category.id == response.id
        assert persisted_category.name == "Filme"
        assert persisted_category.description == "Categoria para filmes"
        assert persisted_category.is_active is False
