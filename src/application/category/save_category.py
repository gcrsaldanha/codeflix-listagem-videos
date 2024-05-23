from dataclasses import dataclass
from datetime import datetime
from uuid import UUID

from src.application.category.exceptions import InvalidCategory
from src.domain.category.category import Category
from src.domain.category.category_repository import CategoryRepository


class SaveCategory:
    # Ref: https://github.com/devfullcycle/FC3-catalogo-de-videos-api-java/blob/main/application/src/main/java/com/fullcycle/catalogo/application/category/save/SaveCategoryUseCase.java
    def __init__(self, repository: CategoryRepository):
        self.repository = repository

    @dataclass
    class Input:
        id: UUID
        name: str
        description: str
        is_active: bool
        created_at: datetime
        updated_at: datetime

    @dataclass
    class Output:
        id: UUID

    def execute(self, input: Input) -> Output:
        try:
            category = Category(
                id=input.id,
                name=input.name,
                description=input.description,
                is_active=input.is_active,
                created_at=input.created_at,
                updated_at=input.updated_at,
            )
            self.repository.save(category)
        except ValueError as err:
            raise InvalidCategory(err)

        self.repository.save(category)
        return self.Output(id=category.id)
