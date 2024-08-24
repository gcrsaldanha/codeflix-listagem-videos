from src import config
from src.application.listing import ListInput, ListOutput, ListOutputMeta, SortDirection


def test_list_input_defaults_to_correct_values():
    input_data = ListInput()
    assert input_data.search is None
    assert input_data.page == 1
    assert input_data.per_page == config.DEFAULT_PAGINATION_SIZE
    assert input_data.sort is None
    assert input_data.direction == SortDirection.ASC


def test_list_output_meta_computes_next_page_correctly():
    meta = ListOutputMeta(page=1, per_page=10, total_count=25)
    assert meta.next_page == 2

    meta = ListOutputMeta(page=2, per_page=10, total_count=20)
    assert meta.next_page is None


def test_list_output_defaults_to_correct_values():
    output = ListOutput()
    assert output.data == []
    assert output.meta.page == 1
    assert output.meta.per_page == config.DEFAULT_PAGINATION_SIZE
    assert output.meta.total_count == 0
