from abc import ABC, abstractmethod
from typing import Tuple

from src.application.listing import SortDirection
from src.config import DEFAULT_PAGINATION_SIZE
from src.domain.genre.genre import Genre
from src.domain.repository import Repository


class GenreRepository(Repository):
    @abstractmethod
    def search(
        self,
        page: int = 1,
        per_page: int = DEFAULT_PAGINATION_SIZE,
        search: str | None = None,
        sort: str | None = None,
        direction: SortDirection = SortDirection.ASC,
    ) -> Tuple[list[Genre], int]:
        raise NotImplementedError
