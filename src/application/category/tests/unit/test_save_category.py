from datetime import datetime, timezone
import uuid
from unittest.mock import MagicMock
from uuid import UUID

import pytest

from src.application.category.exceptions import InvalidCategory
from src.application.category.save_category import SaveCategory
from src.domain.category.category_repository import CategoryRepository


class TestSaveCategory:
    def test_save_category(self):
        mock_repository = MagicMock(CategoryRepository)
        use_case = SaveCategory(repository=mock_repository)
        id = uuid.uuid4()
        now = datetime.now(timezone.utc)
        request = SaveCategory.Input(
            id=id,
            name="Filme",
            description="Categoria para filmes",
            is_active=True,
            created_at=now,
            updated_at=now,
        )

        response = use_case.execute(request)

        assert response.id is not None
        assert isinstance(response, SaveCategory.Output)
        assert isinstance(response.id, UUID)
        assert mock_repository.save.called is True

    def test_save_category_with_invalid_data(self):
        use_case = SaveCategory(repository=MagicMock(CategoryRepository))

        invalid_input = SaveCategory.Input(
            id=uuid.uuid4(),
            name="",
            description="",
            is_active=True,
            created_at=datetime.now(timezone.utc),
            updated_at=datetime.now(timezone.utc),
        )
        with pytest.raises(InvalidCategory, match="name cannot be empty") as exc_info:
            use_case.execute(input=invalid_input)

        assert exc_info.type is InvalidCategory
        assert str(exc_info.value) == "name cannot be empty"
