from unittest.mock import create_autospec
from src.infra.kafka.consumer import AbstractClient, Consumer
from confluent_kafka import KafkaException, Consumer as KafkaConsumer, Message


def test_when_new_category_event_then_create_category_in_database():
    pass
    # client = create_autospec(AbstractClient)
    # message = create_autospec(Message)
    # with open("debezium-examples/create.json", "r") as create_event_data:
    #     message.value.return_value = create_event_data.read().encode('utf-8')
    #     message.error.return_value = None

    # client.poll.return_value = message

    # consumer = Consumer(
    #     client=client,
    #     parser=parse_to_save_category,
    # )

    # consumer.start_consuming()
