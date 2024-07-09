from elasticsearch import Elasticsearch


CATEGORY_INDEX = "categories"

INDEXES = [
    CATEGORY_INDEX,
    # "genres",
    # "cast_members",
    # "videos",
]


def get_elasticsearch(host: str = "elasticsearch", port: int = 9200):
    es = Elasticsearch([f"http://{host}:{port}"])

    for index in INDEXES:
        if not es.indices.exists(index=index):
            es.indices.create(index=index)

    return es
