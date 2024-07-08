from elasticsearch import Elasticsearch


def get_elasticsearch(host: str = "elasticsearch", port: int = 9200):
    # TODO: We can make it a singleton if we want to
    # TODO: extract this to env vars later
    es = Elasticsearch([f"http://{host}:{port}"])
    if not es.indices.exists(index="categories"):
        es.indices.create(index="categories")

    return es
