import os

DEFAULT_PAGINATION_SIZE = 5
ELASTICSEARCH_HOST = os.getenv("ELASTICSEARCH_HOST", "http://localhost:9200")
ELASTICSEARCH_TEST_HOST = os.getenv("ELASTICSEARCH_TEST_HOST", "http://localhost:9201")
KAFKA_HOST = os.getenv("KAFKA_HOST", "http://localhost:9092")
