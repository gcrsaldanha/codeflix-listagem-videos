from abc import ABC

from src.domain.genre.genre import Genre
from src.domain.repository import Repository


class GenreRepository(Repository[Genre], ABC):
    pass
