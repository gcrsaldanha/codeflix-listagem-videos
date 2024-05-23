from fastapi import HTTPException, APIRouter

from src.api.models import Category
from src.application.category.list_category import ListCategory
from src.infra.elasticsearch.category_elastic_repository import CategoryElasticRepository
from src.infra.elasticsearch.client import get_elasticsearch

router = APIRouter()


@router.get("/", response_model=list[Category])
def list_categories():
    try:
        list_use_case = ListCategory(repository=CategoryElasticRepository())
        output = list_use_case.execute(input=ListCategory.Input())
        return output.data
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/", response_model=Category)
def save_category(category: Category):  # Is it called whatsoever? Why does GraphQLController would call save?
    data = {
        "id": category.id,
        "name": category.name,
        "description": category.description,
        "is_active": category.is_active,
        "created_at": category.created_at,
        "updated_at": category.created_at,
    }
    # TODO: UseCase -> Gateway (Repository?) -> Elasticsearch
    # Index the category in Elasticsearch
    get_elasticsearch().index(index="categories", id=str(category.id), body=data)
    return category
