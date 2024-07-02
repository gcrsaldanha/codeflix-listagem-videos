import pytest
from testcontainers.elasticsearch import ElasticSearchContainer


@pytest.mark.skip
def test_list_categories():
    with ElasticSearchContainer("elasticsearch:8.13.4", mem_limit="1G") as es:
        pass

