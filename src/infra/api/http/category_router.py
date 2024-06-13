from fastapi import HTTPException, APIRouter, Query

from src.application.category.list_category import ListCategory
from src.application.listing import ListOutput
from src.infra.api.models import Category
from src.infra.elasticsearch.category_elastic_repository import CategoryElasticRepository
from src.infra.elasticsearch.client import get_elasticsearch

router = APIRouter()


@router.get("/", response_model=ListOutput)
def list_categories(
    search: str | None = Query(None, description="Search term for name or description"),
    page: int = Query(1, ge=1, description="Page number"),
    per_page: int = Query(10, ge=1, le=100, description="Number of items per page"),
    sort: str | None = Query(None, description="Field to sort by"),
    direction: str = Query("asc", regex="^(asc|desc)$", description="Sort direction (asc or desc)"),
):
    list_use_case = ListCategory(repository=CategoryElasticRepository())
    input_data = ListCategory.Input(
        search=search,
        page=page,
        per_page=per_page,
        sort=sort,
        direction=direction,
    )
    output = list_use_case.execute(input=input_data)
    return ListOutput(data=output.data, meta=output.meta)


@router.post("/", response_model=Category)
def save_category(category: Category):
    data = {
        "id": category.id,
        "name": category.name,
        "description": category.description,
        "is_active": category.is_active,
        "created_at": category.created_at,
        "updated_at": category.created_at,
    }
    get_elasticsearch().index(index="categories", id=str(category.id), body=data)
    return category
