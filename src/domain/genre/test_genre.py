import uuid
from datetime import datetime, timezone

import pytest
from pydantic import ValidationError

from src.domain.factories import GenreFactory, CategoryFactory
from src.domain.genre.genre import Genre


class TestGenre:
    def test_name_must_have_less_than_255_characters(self):
        with pytest.raises(ValueError, match="String should have at most 255 characters"):
            GenreFactory(name="a" * 256)

    def test_create_genre_with_provided_values(self):
        genre_id = uuid.uuid4()
        now = datetime.now(timezone.utc)

        film = CategoryFactory(name="Film")
        documentary = CategoryFactory(name="Documentary")

        genre = Genre(
            id=genre_id,
            name="Drama",
            is_active=False,
            created_at=now,
            updated_at=now,
            categories={film.id, documentary.id},
        )

        assert genre.id == genre_id
        assert genre.name == "Drama"
        assert genre.is_active is False
        assert genre.created_at == now
        assert genre.updated_at == now

        assert genre.categories == {film.id, documentary.id}

    def test_cannot_create_genre_with_empty_name(self):
        with pytest.raises(ValidationError) as exc_info:
            GenreFactory(name="")

        assert exc_info.value.errors()[0]["loc"] == ("name",)
        assert exc_info.value.errors()[0]["msg"] == "String should have at least 1 character"

    def test_multiple_validation_errors(self):
        with pytest.raises(ValueError) as exc_info:
            GenreFactory(name="", categories={1})  # Invalid UUID

        assert exc_info.value.error_count() == 2

    def test_create_genre_without_categories(self):
        genre = GenreFactory(categories=set())

        assert genre.categories == set()


class TestEquality:
    def test_when_genres_have_same_id_they_are_equal(self):
        common_id = uuid.uuid4()
        genre_1 = GenreFactory(name="Drama", id=common_id)
        genre_2 = GenreFactory(name="Comedy", id=common_id)

        assert genre_1 == genre_2

    def test_equality_different_classes(self):
        class Dummy:
            pass

        common_id = uuid.uuid4()
        genre = GenreFactory(name="Drama", id=common_id)
        dummy = Dummy()
        dummy.id = common_id

        assert genre != dummy


class TestToDict:
    def test_to_dict(self):
        category_film = CategoryFactory(name="Film")
        category_documentary = CategoryFactory(name="Documentary")
        genre = GenreFactory(name="Drama", categories={category_film.id, category_documentary.id})
        genre_dict = genre.to_dict()

        assert genre_dict["id"] == genre.id
        assert genre_dict["name"] == "Drama"
        assert genre_dict["categories"] == [str(category_film.id), str(category_documentary.id)]
        assert genre_dict["is_active"] is True
        assert genre_dict["created_at"] == genre.created_at
        assert genre_dict["updated_at"] == genre.updated_at
        assert isinstance(genre_dict["created_at"], datetime)
        assert isinstance(genre_dict["updated_at"], datetime)


class TestFromDict:
    def test_from_dict(self):
        category_film_id = uuid.uuid4()
        category_documentary_id = uuid.uuid4()
        genre_id = uuid.uuid4()
        now_as_str = "2021-08-01T00:00:00Z"

        genre_dict = {
            "id": genre_id,
            "name": "Drama",
            "categories": {category_film_id, category_documentary_id},
            "is_active": True,
            "created_at": now_as_str,
            "updated_at": now_as_str,
        }

        expected_genre = Genre(
            id=genre_dict["id"],
            name="Drama",
            is_active=True,
            created_at=datetime.fromisoformat(now_as_str),
            updated_at=datetime.fromisoformat(now_as_str),
            categories={category_film_id, category_documentary_id},
        )

        assert Genre.from_dict(data=genre_dict) == expected_genre
