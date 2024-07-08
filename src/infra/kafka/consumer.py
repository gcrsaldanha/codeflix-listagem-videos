from abc import ABC, abstractmethod
from enum import StrEnum
from typing import Callable, Literal, Type
from pydantic.dataclasses import dataclass
from decimal import Decimal
import json
import os
from confluent_kafka import KafkaException, Consumer as KafkaConsumer, Message
import logging

from src.application.category.save_category import SaveCategory
from src.domain.category.category import Category
from src.infra.elasticsearch.category_elastic_repository import CategoryElasticRepository


# Configuration for the Kafka consumer
config = {
    "bootstrap.servers": os.getenv('BOOTSTRAP_SERVERS', 'kafka:19092'),
    "group.id": "consumer-cluster",
    "auto.offset.reset": "earliest",
}
topics = [
    "catalog-db.codeflix.categories",
]

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)



class AbstractClient(ABC):
    def __init__(self, config: dict, topics: list):
        self.config = config
        self.topics = topics

    @abstractmethod
    def close(self):
        pass

    @abstractmethod
    def poll(self, timeout: float) -> Message:
        pass

    @abstractmethod
    def commit(self, message: Message):
        pass


class Operation(StrEnum):
    CREATE = "c"
    UPDATE = "u"
    DELETE = "d"
    READ = "r"


@dataclass
class ParsedEvent:
    entity: Type[Category]  # Add other entities: CastMember, Genre, Video
    operation: Operation
    payload: dict



table_to_entity = {
    "categories": Category,
    # "cast_members": CastMember,
    # "genres": Genre,
    # "videos": Video,
}


class AbstractEventHandler(ABC):
    @abstractmethod
    def handle_created(self, event: ParsedEvent) -> None:
        pass

    @abstractmethod
    def handle_updated(self, event: ParsedEvent) -> None:
        pass

    @abstractmethod
    def handle_deleted(self, event: ParsedEvent) -> None:
        pass


class CategoryEventHandler(AbstractEventHandler):
    def handle_created(self, event: ParsedEvent) -> None:
        print(f"Category payload: {event.payload}")
        input = SaveCategory.Input(
            category=Category(
                id=event.payload['external_id'],
                name=event.payload['name'],
                description=event.payload['description'],
                created_at=event.payload['created_at'],
                updated_at=event.payload['updated_at'],
                is_active=event.payload['is_active'],
            )
        )
        use_case = SaveCategory(repository=CategoryElasticRepository())
        use_case.execute(input=input)

    def handle_updated(self, event: ParsedEvent) -> None:
        print(f"Updating category: {event.payload}")

    def handle_deleted(self, event: ParsedEvent) -> None:
        print(f"Deleting category: {event.payload}")


entity_to_handler = {
    Category: CategoryEventHandler,
    # CastMember: CastMemberEventHandler,
    # Genre: GenreEventHandler,
    # Video: VideoEventHandler,
}


def parse_debezium_message(data: bytes) -> ParsedEvent | None:
    try:
        data = json.loads(data.decode('utf-8'))
    except json.JSONDecodeError as e:
        logger.error(e)
        return None

    try:
        entity = table_to_entity[data["payload"]["source"]["table"]]
        operation = Operation(data["payload"]["op"])
        payload = data["payload"]["after"] if operation != Operation.DELETE else data["payload"]["before"]
    except (KeyError, ValueError) as e:
        logger.error(e)
        return None

    return ParsedEvent(entity, operation, payload)


class Consumer:
    def __init__(
        self,
        client: AbstractClient,
        parser: Callable[[bytes], ParsedEvent | None],
    ) -> None:
        self.client = client
        self.parser = parser

    def start_consuming(self, topics: list[str]):
        logger.info("Starting consumer...")
        try:
            self.client.subscribe(topics=topics)
            while True:
                message = self.client.poll(timeout=1.0)
                if message is None:
                    continue
                if message.error():
                    logger.error(message.error())
                    continue

                message_data = message.value()
                if not message_data:  # delete event send message with `None`
                    continue

                print(f"Received event: {message_data}")
                self.consume(message_data)
                self.client.commit(message=message)
        except KeyboardInterrupt:
            logger.info("Stopping consumer...")
            self.stop_consuming()
        except KafkaException as e:
            logger.error(e)
        finally:
            self.stop_consuming()

    def consume(self, data: bytes) -> None:
        parsed_event = self.parser(data)
        if parsed_event is None:
            logger.error("Failed to parse event from data: {data}")
            return

        handler = entity_to_handler[parsed_event.entity]()
        if parsed_event.operation == Operation.CREATE:
            handler.handle_created(parsed_event)
        elif parsed_event.operation == Operation.UPDATE:
            handler.handle_updated(parsed_event)
        elif parsed_event.operation == Operation.DELETE:
            handler.handle_deleted(parsed_event)
        else:
            logger.info(f"Unknown operation: {parsed_event.operation}")

    def stop_consuming(self):
        logger.info("Closing consumer...")
        self.client.close()


if __name__ == "__main__":
    client = KafkaConsumer(config)
    consumer = Consumer(client=client, parser=parse_debezium_message)
    consumer.start_consuming(topics=topics)
