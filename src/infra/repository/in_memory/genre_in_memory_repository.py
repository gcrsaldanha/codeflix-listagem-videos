from typing import List

from src.application.listing import SortDirection
from src.config import DEFAULT_PAGINATION_SIZE
from src.domain.genre.genre import Genre
from src.domain.genre.genre_repository import GenreRepository


class GenreInMemoryRepository(GenreRepository):
    def __init__(self, genres: list[Genre] | None = None):
        self.genres: list[Genre] = genres or []

    def save(self, entity: Genre) -> None:
        if entity not in self.genres:
            self.genres.append(entity)
        else:
            self.genres[self.genres.index(entity)] = entity

    def search(
        self,
        page: int = 1,
        per_page: int = DEFAULT_PAGINATION_SIZE,
        search: str | None = None,
        sort: str | None = None,
        direction: SortDirection = SortDirection.ASC,
    ) -> tuple[list[Genre], int]:
        genres: List[Genre] = [genre for genre in self.genres]
        total_count = len(genres)

        if search:
            genres = [genre for genre in genres if search.upper() in genre.name.upper()]

        if sort:
            genres = sorted(genres, key=lambda genre: getattr(genre, sort), reverse=direction == SortDirection.DESC)

        ent_page = genres[(page - 1) * per_page : (page * per_page)]
        return ent_page, total_count
