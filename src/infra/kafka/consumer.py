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


# def basic_consume_loop(consumer, topics):
#     logger.info("Consume loop...")
#     try:
#         consumer.subscribe(topics)
#
#         while running:
#             msg = consumer.poll(timeout=1.0)
#             if msg is None:
#                 continue
#
#             logger.info("Got a message!")
#             if msg.error():
#                 if msg.error().code() == KafkaError._PARTITION_EOF:
#                     # End of partition event
#                     sys.stderr.write(
#                         "%% %s [%d] reached end at offset %d\n" % (msg.topic(), msg.partition(), msg.offset())
#                     )
#                 elif msg.error():
#                     raise KafkaException(msg.error())
#             else:
#                 category_input = SaveCategory.Input(
#                     id=uuid.uuid4(),
#                     name=msg.value().decode(),
#                     description="",
#                     is_active=True,
#                     created_at=datetime.now(),
#                     updated_at=datetime.now(),
#                 )
#                 use_case = SaveCategory(repository=CategoryElasticRepository())
#                 use_case.execute(category_input)
#                 logger.info(msg.value())
#                 logger.info(f"Category {category_input.id} saved!")
#
#     finally:
#         # Close down consumer to commit final offsets.
#         consumer.close()
