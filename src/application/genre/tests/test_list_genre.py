from src.application.genre.list_genre import ListGenre
from src.application.listing import ListOutputMeta
from src.domain.factories import CategoryFactory, GenreFactory
from src.infra.elasticsearch.genre_in_memory_repository import GenreInMemoryRepository


class TestListGenre:
    def test_when_no_genres_then_return_empty_list(self) -> None:
        empty_repository = GenreInMemoryRepository()
        use_case = ListGenre(repository=empty_repository)
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

        repository = GenreInMemoryRepository()
        repository.save(genre_drama)
        repository.save(genre_comedy)

        use_case = ListGenre(repository=repository)
        response = use_case.execute(
            input=ListGenre.Input(
                per_page=1,
            )
        )

        assert response == ListGenre.Output(
            data=[genre_comedy],
            meta=ListOutputMeta(
                total_count=2,
                page=1,
                per_page=1,
            ),
        )
        assert response.data[0].categories == {category_film.id}
        assert response.meta.next_page == 2
