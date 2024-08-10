from src.application.category.list_category import ListCategory
from src.domain.category.category import Category
from src.infra.elasticsearch.category_elastic_repository import CategoryElasticRepository


def list_categories() -> list[Category]:
    repository = CategoryElasticRepository()
    use_case = ListCategory(repository=repository)
    output = use_case.execute(input=ListCategory.Input())

    return [category for category in output.data]
