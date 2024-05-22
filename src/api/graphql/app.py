from uuid import UUID

import strawberry
from strawberry.fastapi import GraphQLRouter


@strawberry.type
class Category:
    id: UUID
    name: str
    description: str
    is_active: bool
    created_at: str
    updated_at: str


def list_categories():
    return [
        Category(
            id=UUID("123e4567-e89b-12d3-a456-426614174000"),
            name="Category Name",
            description="Category Description",
            is_active=True,
            created_at="2023-01-01T00:00:00",
            updated_at="2023-01-01T00:00:00",
        ),
        Category(
            id=UUID("124e4567-e89b-12d3-a456-426614174000"),
            name="Category Name",
            description="Category Description",
            is_active=True,
            created_at="2023-01-01T00:00:00",
            updated_at="2023-01-01T00:00:00",
        )
    ]


@strawberry.type
class Query:
    categories: list[Category] = strawberry.field(resolver=list_categories)


schema = strawberry.Schema(query=Query)

graphql_app = GraphQLRouter(schema)

# Run: strawberry server src.api.graphql.app.schema --port 8001
