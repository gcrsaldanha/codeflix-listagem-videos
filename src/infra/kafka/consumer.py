import logging
import sys
import uuid
from datetime import datetime

from confluent_kafka import KafkaException, KafkaError, Consumer

from src.application.category.save_category import SaveCategory
from src.infra.elasticsearch.category_elastic_repository import CategoryElasticRepository

running = True

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

conf = {'bootstrap.servers': 'kafka:19092', 'group.id': '1'}
consumer = Consumer(conf)


def basic_consume_loop(consumer, topics):
    logger.info("Consume loop...")
    try:
        consumer.subscribe(topics)

        while running:
            msg = consumer.poll(timeout=1.0)
            if msg is None:
                continue

            logger.info("Got a message!")
            if msg.error():
                if msg.error().code() == KafkaError._PARTITION_EOF:
                    # End of partition event
                    sys.stderr.write('%% %s [%d] reached end at offset %d\n' %
                                     (msg.topic(), msg.partition(), msg.offset()))
                elif msg.error():
                    raise KafkaException(msg.error())
            else:
                category_input = SaveCategory.Input(
                    id=uuid.uuid4(),
                    name=msg.value().decode(),
                    description="",
                    is_active=True,
                    created_at=datetime.now(),
                    updated_at=datetime.now(),
                )
                use_case = SaveCategory(repository=CategoryElasticRepository())
                use_case.execute(category_input)
                logger.info(msg.value())
                logger.info(f"Category {category_input.id} saved!")

    finally:
        # Close down consumer to commit final offsets.
        consumer.close()


def shutdown():
    running = False
