import logging

from fastapi import APIRouter, Depends, Query, Response
from pydantic import ValidationError

from src import config
from src.application.exceptions import SearchError
from src.application.genre.list_genre import ListGenre, SortableFields
from src.application.listing import ListOutput, SortDirection
from src.domain.genre.genre_repository import GenreRepository
from src.infra.repository.elastic.genre_elastic_repository import GenreElasticRepository

logger = logging.getLogger(__name__)

router = APIRouter()


def get_repository() -> GenreRepository:
    return GenreElasticRepository()


@router.get("/", response_model=ListOutput)
def list_genres(
    search: str | None = Query(None, description="Search term for name or description"),
    page: int = Query(1, ge=1, description="Page number"),
    per_page: int = Query(config.DEFAULT_PAGINATION_SIZE, ge=1, le=100, description="Number of items per page"),
    sort: SortableFields = Query(SortableFields.NAME, description="Field to sort by"),
    direction: SortDirection = Query(SortDirection.ASC, description="Sort direction (asc or desc)"),
    repository: GenreRepository = Depends(get_repository),
) -> ListOutput | Response:
    list_use_case = ListGenre(repository=repository)
    try:
        input_data = ListGenre.Input(
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
        return Response(status_code=500, content="Error when searching genres")
    return ListOutput(data=output.data, meta=output.meta)
