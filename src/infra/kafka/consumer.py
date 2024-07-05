from abc import ABC, abstractmethod
from enum import StrEnum
from typing import Literal
from pydantic.dataclasses import dataclass
from decimal import Decimal
import json
import os
from confluent_kafka import KafkaException, Consumer as KafkaConsumer, Message
import logging

from src.application.category.save_category import SaveCategory
from src.domain.category.category import Category


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


def parse_to_save_category(data: dict) -> SaveCategory.Input:
    return SaveCategory.Input(
        category=Category(
            id=data['id'],
            name=data['name'],
            description=data['description'],
            created_at=data['created_at'],
            updated_at=data['updated_at'],
            is_active=data['is_active'],
        )
    )


class Consumer:
    def __init__(self, client: AbstractClient, parser: callable):
        self.client = client
        self.parser = parser

    def start_consuming(self):
        try:
            while True:
                message = self.client.poll(timeout=1.0)
                if message is None:
                    continue
                if message.error():
                    logger.error(message.error())
                    continue

                print(f"Received event: {data}")
                data = self.parser(message.value())

                self.consume(data)

                self.client.commit(message=message)
        except KeyboardInterrupt:
            logger.info("Stopping consumer...")
            self.stop_consuming()
        except KafkaException as e:
            logger.error(e)
        finally:
            self.stop_consuming()

    def consume(message_data: bytes):
        data = json.loads(message_data.decode('utf-8'))
        return SaveCategory.Input(
            category=Category(
                id=data['id'],
                name=data['name'],
                description=data['description'],
                created_at=data['created_at'],
                updated_at=data['updated_at'],
                is_active=data['is_active'],
            )
        )


    def stop_consuming(self):
        self.client.close()


if __name__ == "__main__":
    client = KafkaConsumer(config=config, topics=topics)
    consumer = Consumer(client=client, parser=json.loads)
