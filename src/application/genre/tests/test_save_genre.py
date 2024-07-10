import uuid
from datetime import datetime, timezone
from uuid import UUID

from src.application.genre.save_genre import SaveGenre
from src.domain.factories import GenreFactory
from src.domain.genre.genre import Genre
from src.infra.elasticsearch.genre_in_memory_repository import GenreInMemoryRepository


class TestSaveGenre:
    def test_when_genre_does_not_exist_then_create_it(self):
        repository = GenreInMemoryRepository()
        use_case = SaveGenre(repository=repository)
        id = uuid.uuid4()
        now = datetime.now(timezone.utc)

        request = SaveGenre.Input(
            Genre(
                id=id,
                name="Drama",
                categories=set(),
                is_active=True,
                created_at=now,
                updated_at=now,
            )
        )

        response = use_case.execute(request)

        assert response.id == id
        assert len(repository.genres) == 1

        persisted_genre = repository.genres[0]
        assert persisted_genre.id == response.id
        assert persisted_genre.name == "Drama"
        assert persisted_genre.is_active is True

    def test_when_genre_exists_then_update_it(self):
        repository = GenreInMemoryRepository()
        old_genre = GenreFactory(name="Drama")
        repository.save(old_genre)
        assert len(repository.genres) == 1

        use_case = SaveGenre(repository=repository)
        now = datetime.now(timezone.utc)
        new_categories_set = {uuid.uuid4()}
        request = SaveGenre.Input(
            Genre(
                id=old_genre.id,
                name="Comedy",  # Update to something else
                is_active=False,  # Update to inactive
                categories=new_categories_set,  # Update categories
                created_at=now,
                updated_at=now,
            ),
        )

        response = use_case.execute(request)
        persisted_genre = repository.genres[0]

        assert persisted_genre.id == response.id == old_genre.id
        assert persisted_genre.name == "Comedy"
        assert persisted_genre.is_active is False
        assert persisted_genre.is_active is False
        assert len(repository.genres) == 1
