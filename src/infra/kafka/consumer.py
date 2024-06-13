import logging

from confluent_kafka import KafkaException, Consumer

config = {
    "bootstrap.servers": "kafka:19092",
    "group.id": "consumer-cluster",
    "enable.auto.commit": False,
    "auto.offset.reset": "earliest",
}
topics = [
    "catalog-db.codeflix.categories",
]

running = True

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def assignment_callback(consumer, partitions):
    # Passed to `consumer.subscribe()` to get the initial assignment.
    # Invoked when partitions are assigned to this consumer
    # This includes when rebalancing occurs as well
    logger.info("Assignment callback: {}".format(partitions))
    for p in partitions:
        print(f"Assigned to {p.topic} [{p.partition}]")


if __name__ == "__main__":
    consumer = Consumer(config)
    consumer.subscribe(topics, on_assign=assignment_callback)

    try:
        while True:
            message = consumer.poll(timeout=1.0)
            if message is None:
                continue

            if message.error():
                raise KafkaException(message.error())
            else:
                val = message.value().decode("utf-8")
                partition = message.partition()
                print(f"Received event: {val} from partition {partition}")
                consumer.commit(message=message)
    except KeyboardInterrupt:
        print("Interrupted by user")
    finally:
        consumer.close()
