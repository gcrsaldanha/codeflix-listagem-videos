import strawberry

from src.infra.api.graphql.resolvers import list_categories
from src.infra.api.models import Category


@strawberry.experimental.pydantic.type(model=Category, all_fields=True)
class GraphQLCategory(Category):
    pass


@strawberry.type
class Query:
    categories: list[GraphQLCategory] = strawberry.field(resolver=list_categories)


schema = strawberry.Schema(query=Query)
