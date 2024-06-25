from datetime import datetime, timezone
import uuid
from unittest.mock import MagicMock
from uuid import UUID

import pytest

from src.application.category.exceptions import InvalidCategory
from src.application.category.save_category import SaveCategory
from src.domain.category.category import Category
from src.domain.category.category_repository import CategoryRepository


class TestSaveCategory:
    def test_save_category(self):
        mock_repository = MagicMock(CategoryRepository)
        use_case = SaveCategory(repository=mock_repository)
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

        assert response.id is not None
        assert isinstance(response, SaveCategory.Output)
        assert isinstance(response.id, UUID)
        assert mock_repository.save.called is True
