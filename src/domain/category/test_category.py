import uuid
from datetime import datetime, timezone
from uuid import UUID

from pydantic import ValidationError
import pytest

from src.application.category.tests.factories import CategoryFactory
from src.domain.category.category import Category


class TestCategory:
    def test_name_must_have_less_than_255_characters(self):
        with pytest.raises(ValueError, match="String should have at most 255 characters"):
            CategoryFactory(name="a" * 256)

    def test_create_category_with_provided_values(self):
        cat_id = uuid.uuid4()
        now = datetime.now(timezone.utc)
        category = Category(
            id=cat_id,
            name="Filme",
            description="Filmes em geral",
            is_active=False,
            created_at=now,
            updated_at=now,
        )

        assert category.id == cat_id
        assert category.name == "Filme"
        assert category.description == "Filmes em geral"
        assert category.is_active is False
        assert category.created_at == now
        assert category.updated_at == now

    def test_cannot_create_category_with_empty_name(self):
        with pytest.raises(ValidationError) as exc_info:
            CategoryFactory(name="")

        assert exc_info.value.errors()[0]["loc"] == ("name",)
        assert exc_info.value.errors()[0]["msg"] == "String should have at least 1 character"

    def test_cannot_create_category_with_description_longer_than_1024(self):
        with pytest.raises(ValueError, match="String should have at most 1024 characters"):
            CategoryFactory(name="Filme", description="a" * 1025)

    def test_multiple_validation_errors(self):
        with pytest.raises(ValueError) as exc_info:
            CategoryFactory(name="", description="a" * 1025)

        assert exc_info.value.error_count() == 2


class TestEquality:
    def test_when_categories_have_same_id_they_are_equal(self):
        common_id = uuid.uuid4()
        category_1 = CategoryFactory(name="Filme", id=common_id)
        category_2 = CategoryFactory(name="Outro filme", id=common_id)

        assert category_1 == category_2

    def test_equality_different_classes(self):
        class Dummy:
            pass

        common_id = uuid.uuid4()
        category = CategoryFactory(name="Filme", id=common_id)
        dummy = Dummy()
        dummy.id = common_id

        assert category != dummy
