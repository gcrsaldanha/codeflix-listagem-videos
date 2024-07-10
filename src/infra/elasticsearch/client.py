from elasticsearch import Elasticsearch

from src.config import ELASTICSEARCH_HOST

CATEGORY_INDEX = "categories"

INDEXES = [
    CATEGORY_INDEX,
    # "genres",
    # "cast_members",
    # "videos",
]


_es_instance = None


def get_elasticsearch(host: str = ""):
    global _es_instance

    if _es_instance is None:
        _es_instance = Elasticsearch([host or ELASTICSEARCH_HOST])

        for index in INDEXES:
            if not _es_instance.indices.exists(index=index):
                _es_instance.indices.create(index=index)

    return _es_instance
