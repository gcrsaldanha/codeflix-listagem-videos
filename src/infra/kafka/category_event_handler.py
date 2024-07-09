import logging

from src.application.category.save_category import SaveCategory
from src.domain.category.category import Category
from src.infra.elasticsearch.category_elastic_repository import CategoryElasticRepository
from src.infra.kafka.abstract_event_handler import AbstractEventHandler
from src.infra.kafka.parser import ParsedEvent

logger = logging.getLogger(__name__)


class CategoryEventHandler(AbstractEventHandler):  # Similar to a View in Django
    def __init__(self, save_use_case: SaveCategory | None = None):
        self.save_use_case = save_use_case or SaveCategory(repository=CategoryElasticRepository())

    def _handle_update_or_create(self, event: ParsedEvent) -> None:
        input = SaveCategory.Input(
            category=Category(
                id=event.payload["external_id"],
                name=event.payload["name"],
                description=event.payload["description"],
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
