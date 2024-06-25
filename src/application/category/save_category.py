from dataclasses import dataclass
from uuid import UUID

from pydantic import ValidationError

from src.application.category.exceptions import InvalidCategory
from src.domain.category.category import Category
from src.domain.category.category_repository import CategoryRepository


class SaveCategory:
    # Ref: https://github.com/devfullcycle/FC3-catalogo-de-videos-api-java/blob/main/application/src/main/java/com/fullcycle/catalogo/application/category/save/SaveCategoryUseCase.java
    def __init__(self, repository: CategoryRepository):
        self.repository = repository

    @dataclass
    class Input:
        category: Category

    @dataclass
    class Output:
        id: UUID

    def execute(self, input: Input) -> Output:
        try:
            self.repository.save(input.category)
        except ValidationError as validation_error:
            # TODO: adapt this for GraphQL
            raise InvalidCategory(validation_error)
        else:
            return self.Output(id=input.category.id)
