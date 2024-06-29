import json
from testcontainers.elasticsearch import ElasticSearchContainer
import urllib3


def test_list_categories():
    with ElasticSearchContainer("elasticsearch:8.13.4", mem_limit="3G") as es:
        pass

