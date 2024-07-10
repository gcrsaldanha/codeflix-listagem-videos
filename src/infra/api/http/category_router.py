import logging

from fastapi import APIRouter, Depends, Query, Response
from pydantic import ValidationError

from src import config
from src.application.category.exceptions import SearchError
from src.application.category.list_category import ListCategory, SortableFields
from src.application.listing import ListOutput, SortDirection
from src.domain.category.category import Category
from src.infra.elasticsearch.category_elastic_repository import CategoryElasticRepository

logger = logging.getLogger(__name__)

router = APIRouter()


def get_repository() -> CategoryElasticRepository:
    return CategoryElasticRepository()


@router.get("/", response_model=ListOutput)
def list_categories(
    search: str | None = Query(None, description="Search term for name or description"),
    page: int = Query(1, ge=1, description="Page number"),
    per_page: int = Query(config.DEFAULT_PAGINATION_SIZE, ge=1, le=100, description="Number of items per page"),
    sort: SortableFields = Query(SortableFields.NAME, description="Field to sort by"),
    direction: SortDirection = Query(SortDirection.ASC, description="Sort direction (asc or desc)"),
    repository: CategoryElasticRepository = Depends(get_repository),
) -> ListOutput | Response:
    # TODO: common parameters as Dependency - see https://fastapi.tiangolo.com/tutorial/dependencies/#create-a-dependency-or-dependable
    list_use_case = ListCategory(repository=repository)
    try:
        input_data = ListCategory.Input(
            search=search,
            page=page,
            per_page=per_page,
            sort=sort,
            direction=direction,
        )
    except ValidationError as validation_error:
        return Response(status_code=400, content=validation_error.json())

    try:
        output = list_use_case.execute(input=input_data)
    except SearchError as err:
        logger.error(f"Search error: {err}", exc_info=True)
        return Response(status_code=500, content="Error when searching categories")
    return ListOutput(data=output.data, meta=output.meta)


@router.post("/", response_model=Category)
def save_category(category: Category, repository: CategoryElasticRepository = Depends(get_repository)) -> Category:
    data = {
        "id": category.id,
        "name": category.name,
        "description": category.description,
        "is_active": category.is_active,
        "created_at": category.created_at,
        "updated_at": category.updated_at,
    }
    repository.client.index(index="categories", id=str(category.id), body=data)
    return category
