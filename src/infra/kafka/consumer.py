import os
from confluent_kafka import KafkaException, Consumer
import logging

# Configuration for the Kafka consumer
config = {
    "bootstrap.servers": os.getenv('BOOTSTRAP_SERVERS', 'kafka:19092'),
    "group.id": "consumer-cluster",
    "auto.offset.reset": "earliest",
}
topics = [
    "catalog-db.codeflix.categories",
]

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# KafkaConsumer class encapsulates Kafka consumer logic
class KafkaConsumer:
    def __init__(self, config: dict, topics: list[str]):
        self.__consumer = Consumer(config)
        self.__consumer.subscribe(topics)
        self.running = True

    def start_consuming(self):
        while self.running:
            message = self.__consumer.poll(timeout=1.0)
            if message is None:
                continue
            if message.error():
                logger.error(message.error())
            else:
                val = message.value().decode("utf-8")
                print(f"Received event: {val}")
                self.__consumer.commit(message=message)

    def stop_consuming(self):
        self.running = False
        self.__consumer.close()

# Main execution block
if __name__ == "__main__":
    consumer = KafkaConsumer(config=config, topics=topics)
    try:
        consumer.start_consuming()
    except KeyboardInterrupt:
        consumer.stop_consuming()
