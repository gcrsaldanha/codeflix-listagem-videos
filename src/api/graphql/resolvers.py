from src.api.fastapi.dependencies import get_elasticsearch
from src.api.models import Category
from src.application.category.list_category import ListCategory
from src.infra.elasticsearch.category_elastic_repository import CategoryElasticRepository


def list_categories():
    repository = CategoryElasticRepository(client=get_elasticsearch())
    use_case = ListCategory(repository=repository)
    output = use_case.execute(input=ListCategory.Input())

    # TODO: create mappers/serializers
    return [
        Category(
            id=category.id,
            name=category.name,
            description=category.description,
            is_active=category.is_active,
            created_at=category.created_at,
            updated_at=category.updated_at,
        ) for category in output.data
    ]
