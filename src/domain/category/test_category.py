import uuid
from uuid import UUID

import pytest

from src.domain.category.category import Category


class TestCategory:
    def test_name_is_required(self):
        with pytest.raises(
                TypeError, match="missing 1 required positional argument: 'name'"
        ):
            Category()

    def test_name_must_have_less_than_255_characters(self):
        with pytest.raises(ValueError, match="name cannot be longer than 255"):
            Category(name="a" * 256)

    def test_category_must_be_created_with_id_as_uuid_by_default(self):
        category = Category(name="Filme")
        assert isinstance(category.id, UUID)

    def test_create_category_with_default_values(self):
        category = Category(name="Filme")
        assert category.name == "Filme"
        assert category.description == ""
        assert category.is_active is True

    def test_create_category_as_active_by_default(self):
        category = Category(name="Filme")
        assert category.is_active is True

    def test_create_category_with_provided_values(self):
        cat_id = uuid.uuid4()
        category = Category(
            id=cat_id,
            name="Filme",
            description="Filmes em geral",
            is_active=False,
        )

        assert category.id == cat_id
        assert category.name == "Filme"
        assert category.description == "Filmes em geral"
        assert category.is_active is False

    def test_cannot_create_category_with_empty_name(self):
        with pytest.raises(ValueError, match="name cannot be empty"):
            Category(name="")

    def test_cannot_create_cateogry_with_description_longer_than_1024(self):
        with pytest.raises(ValueError, match="description cannot be longer than 1024"):
            Category(name="Filme", description="a" * 1025)

    def test_notification_groups_errors(self):
        with pytest.raises(ValueError, match="name cannot be empty,description cannot be longer than 1024"):
            Category(name="", description="a" * 1025)


class TestEquality:
    def test_when_categories_have_same_id_they_are_equal(self):
        common_id = uuid.uuid4()
        category_1 = Category(name="Filme", id=common_id)
        category_2 = Category(name="Outro filme", id=common_id)

        assert category_1 == category_2

    def test_equality_different_classes(self):
        class Dummy:
            pass

        common_id = uuid.uuid4()
        category = Category(name="Filme", id=common_id)
        dummy = Dummy()
        dummy.id = common_id

        assert category != dummy
