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
logger = logging.getLogger("consumer")



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

    def __call__(self, event: ParsedEvent) -> None:
        if event.operation == Operation.CREATE:
            self.handle_created(event)
        elif event.operation == Operation.UPDATE:
            self.handle_updated(event)
        elif event.operation == Operation.DELETE:
            self.handle_deleted(event)
        else:
            logger.info(f"Unknown operation: {event.operation}")


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
    Category: CategoryEventHandler(),
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
        self.client.subscribe(topics=topics)
        self.parser = parser

    def start(self, topics: list[str]):
        logger.info("Starting consumer...")
        try:
            while True:
                self.consume()
        except KeyboardInterrupt:
            logger.info("Stopping consumer...")
            self.stop()
        except KafkaException as e:
            logger.error(e)
        finally:
            self.stop()

    def consume(self) -> None:
        message = self.client.poll(timeout=1.0)
        if message is None:
            logger.info("No message received")
            return None

        if message.error():
            logger.error("Got message with error: ", message.error())
            return None

        message_data = message.value()
        if not message_data:  # delete event sends two messages, later with `None`
            return None

        logger.info(f"Received message with data: {message_data}")
        parsed_event = self.parser(message_data)
        if parsed_event is None:
            logger.error("Failed to parse event from data: {data}")
            return

        entity_to_handler[parsed_event.entity](parsed_event)
        self.client.commit(message=message)

    def stop(self):
        logger.info("Closing consumer...")
        self.client.close()


if __name__ == "__main__":
    client = KafkaConsumer(config)
    consumer = Consumer(client=client, parser=parse_debezium_message)
    consumer.start(topics=topics)
