import strawberry
from strawberry.fastapi import GraphQLRouter

from src.api.graphql.resolvers import list_categories
from src.api.graphql.schemas import GraphQLCategory


@strawberry.type
class Query:
    categories: list[GraphQLCategory] = strawberry.field(resolver=list_categories)


schema = strawberry.Schema(query=Query)
graphql_app = GraphQLRouter(schema)

# Run: strawberry server src.api.graphql.app.schema --port 8001
