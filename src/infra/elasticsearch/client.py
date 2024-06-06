from elasticsearch import Elasticsearch


def get_elasticsearch():
    # TODO: should it be a singleton?
    es = Elasticsearch(["http://elasticsearch:9200"])
    if not es.indices.exists(index="categories"):
        es.indices.create(index="categories")

    return es
