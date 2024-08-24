from unittest.mock import create_autospec

from src.application.genre.list_genre import ListGenre, SortableFields
from src.application.listing import ListOutputMeta, SortDirection
from src.domain.factories import CategoryFactory, GenreFactory
from src.domain.genre.genre_repository import GenreRepository


class TestListGenre:
    def test_when_no_genres_then_return_empty_list(
        self,
    ) -> None:
        repository = create_autospec(GenreRepository)
        repository.search.return_value = ([], 0)

        use_case = ListGenre(repository=repository)
        response = use_case.execute(input=ListGenre.Input())

        assert response == ListGenre.Output(
            data=[],
            meta=ListOutputMeta(),
        )

    def test_when_genre_exists_then_list_it_with_associated_categories(self) -> None:
        category_film = CategoryFactory(name="Film")
        category_series = CategoryFactory(name="Series")

        genre_drama = GenreFactory(
            name="Drama",
            categories={category_film.id, category_series.id},
        )
        genre_comedy = GenreFactory(
            name="Comedy",
            categories={category_film.id},
        )

        repository = create_autospec(GenreRepository)
        repository.search.return_value = ([genre_drama, genre_comedy], 2)

        use_case = ListGenre(repository=repository)
        response = use_case.execute(
            input=ListGenre.Input(
                per_page=2,
            )
        )

        assert response == ListGenre.Output(
            data=[genre_drama, genre_comedy],
            meta=ListOutputMeta(
                total_count=2,
                page=1,
                per_page=2,
            ),
        )
        assert response.data[0].categories == {category_film.id, category_series.id}
        assert response.meta.next_page is None

        repository.search.assert_called_once_with(
            page=1,
            per_page=2,
            sort=SortableFields.NAME,
            direction=SortDirection.ASC,
            search=None,
        )
