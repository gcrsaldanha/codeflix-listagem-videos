import strawberry

from src.domain.category.category import Category
from src.infra.api.graphql.resolvers import list_categories


@strawberry.experimental.pydantic.type(model=Category, all_fields=True)
class GraphQLCategory(Category):
    pass


@strawberry.type
class Query:
    categories: list[GraphQLCategory] = strawberry.field(resolver=list_categories)


schema = strawberry.Schema(query=Query)
