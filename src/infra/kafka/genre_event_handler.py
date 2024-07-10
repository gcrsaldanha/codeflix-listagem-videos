import logging

from src.application.genre.save_genre import SaveGenre
from src.domain.genre.genre import Genre
from src.infra.elasticsearch.genre_elastic_repository import GenreElasticRepository
from src.infra.kafka.abstract_event_handler import AbstractEventHandler
from src.infra.kafka.parser import ParsedEvent

logger = logging.getLogger(__name__)

"""
1.	cast_member
2.	category
3.	genre
4.	video
5.	genre_categories (for Genre and Category Many-to-Many relationship)
6.	video_categories (for Video and Category Many-to-Many relationship)
7.	video_genres (for Video and Genre Many-to-Many relationship)
8.	video_cast_members (for Video and CastMember Many-to-Many relationship)
"""


class GenreEventHandler(AbstractEventHandler):  # Similar to a View in Django
    def __init__(self, save_use_case: SaveGenre | None = None):
        self.save_use_case = save_use_case or SaveGenre(repository=GenreElasticRepository())

    def _handle_update_or_create(self, event: ParsedEvent) -> None:
        input = SaveGenre.Input(
            genre=Genre(
                id=event.payload["external_id"],
                name=event.payload["name"],
                categories=event.payload["categories"],
                created_at=event.payload["created_at"],
                updated_at=event.payload["updated_at"],
                is_active=event.payload["is_active"],
            )
        )
        self.save_use_case.execute(input=input)

    def handle_created(self, event: ParsedEvent) -> None:
        logger.info(f"Creating category with payload: {event.payload}")
        self._handle_update_or_create(event)

    def handle_updated(self, event: ParsedEvent) -> None:
        logger.info(f"Updating category with payload: {event.payload}")
        self._handle_update_or_create(event)

    def handle_deleted(self, event: ParsedEvent) -> None:
        print(f"Deleting category: {event.payload}")
