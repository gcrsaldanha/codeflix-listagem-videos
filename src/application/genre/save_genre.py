from dataclasses import dataclass
from uuid import UUID

from pydantic import ValidationError

from src.application.exceptions import InvalidEntity
from src.domain.genre.genre import Genre
from src.domain.genre.genre_repository import GenreRepository


class SaveGenre:
    def __init__(
        self,
        repository: GenreRepository,
    ) -> None:
        self.repository = repository

    @dataclass
    class Input:
        genre: Genre

    @dataclass
    class Output:
        id: UUID

    def execute(self, input: Input) -> Output:
        try:
            self.repository.save(input.genre)
        except ValidationError as validation_error:
            raise InvalidEntity(validation_error)
        else:
            return self.Output(id=input.genre.id)
