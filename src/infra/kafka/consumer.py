from typing import Callable, Type
import os
from confluent_kafka import KafkaException, Consumer as KafkaConsumer
import logging

from src.config import KAFKA_HOST
from src.domain.category.category import Category
from src.domain.entity import Entity
from src.domain.genre.genre import Genre
from src.infra.kafka.abstract_event_handler import AbstractEventHandler
from src.infra.kafka.category_event_handler import CategoryEventHandler
from src.infra.kafka.genre_event_handler import GenreEventHandler
from src.infra.kafka.parser import ParsedEvent, parse_debezium_message

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("consumer")

# Configuration for the Kafka consumer
config = {
    "bootstrap.servers": KAFKA_HOST,
    "group.id": "consumer-cluster",
    "auto.offset.reset": "earliest",
}
topics = [
    "catalog-db.codeflix.categories",
    "catalog-db.codeflix.genres",
    # "catalog-db.codeflix.cast_members",
    # "catalog-db.codeflix.videos",
]

# Similar to a "router" -> calls proper handler, each handler will call its specific method according to operation
entity_to_handler: dict[Type[Entity], Type[AbstractEventHandler]] = {
    Category: CategoryEventHandler,
    Genre: GenreEventHandler,
    # CastMember: CastMemberEventHandler,
    # Video: VideoEventHandler,
}


class Consumer:
    def __init__(
        self,
        client: KafkaConsumer,
        parser: Callable[[bytes], ParsedEvent | None],
        router: dict[Type[Entity], Type[AbstractEventHandler]] | None = None,
    ) -> None:
        """
        :param client: Kafka consumer client
        :param parser: Function to parse the message data to a ParsedEvent
        :param router:  Dictionary to route the event to the proper handler
        """
        self.client = client
        self.parser = parser
        self.router = router or entity_to_handler

    def start(self):
        logger.info("Starting consumer...")
        try:
            while True:
                self.consume()
        except KeyboardInterrupt:
            logger.info("Stopping consumer...")
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
            logger.error(f"received message with error: {message.error()}")
            return None

        message_data = message.value()
        if not message_data:
            return None

        logger.info(f"Received message with data: {message_data}")
        parsed_event = self.parser(message_data)
        if parsed_event is None:
            logger.error(f"Failed to parse message data: {message_data}")
            return

        # Call the proper handler
        handler = self.router[parsed_event.entity]()
        handler(parsed_event)

        self.client.commit(message=message)

    def stop(self):
        logger.info("Closing consumer...")
        self.client.close()


if __name__ == "__main__":
    kafka_consumer = KafkaConsumer(config)
    kafka_consumer.subscribe(topics=topics)
    consumer = Consumer(client=kafka_consumer, parser=parse_debezium_message)
    consumer.start()
