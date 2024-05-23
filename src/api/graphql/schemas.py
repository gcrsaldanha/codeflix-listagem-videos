import strawberry

from src.api.models import Category as BaseCategory


@strawberry.experimental.pydantic.type(model=BaseCategory, all_fields=True)
class GraphQLCategory(BaseCategory):
    pass
