from elasticsearch import Elasticsearch

from src.config import ELASTICSEARCH_HOST

CATEGORY_INDEX = "catalog-db.codeflix.categories"
GENRE_INDEX = "catalog-db.codeflix.genres"
GENRE_CATEGORY_INDEX = "catalog-db.codeflix.genre_categories"

INDEXES = [
    CATEGORY_INDEX,
    GENRE_INDEX,
    GENRE_CATEGORY_INDEX,
]

_es_instance = None


def get_elasticsearch(host: str = "") -> Elasticsearch:
    global _es_instance

    if _es_instance is None:
        _es_instance = Elasticsearch([host or ELASTICSEARCH_HOST])

        for index in INDEXES:
            if not _es_instance.indices.exists(index=index):
                _es_instance.indices.create(index=index)
                print(f"Created index: {index}")

        # Create a index template for UUID fields (keyword)
        if _es_instance.indices.exists_template(name="uuid_template"):
            _es_instance.indices.delete_template(name="uuid_template")
            print("Deleted existing uuid_template.")

        template_body = {
            "index_patterns": ["catalog-db.codeflix.*"],  # Specific to your indexes
            "template": {"mappings": {"properties": {"id": {"type": "keyword"}}}},
        }
        _es_instance.indices.put_index_template(name="uuid_template", body=template_body)

    return _es_instance
