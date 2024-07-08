import pytest
from src.infra.kafka.consumer import parse_debezium_message, ParsedEvent, Operation, Category

class TestParseDebeziumMessage:
    def test_parse_created_message(self):
        data = b'{"payload": {"source": {"table": "categories"}, "op": "c", "after": {"id": 1, "external_id": "d5889ed5-3d3f-11ef-baf5-0242ac130006", "name": "Category 1", "description": "Description 1", "created_at": "2022-01-01", "updated_at": "2022-01-01", "is_active": true}}}'
        parsed_event = parse_debezium_message(data)
        expected_event = ParsedEvent(
            entity=Category,
            operation=Operation.CREATE,
            payload={
                "id": 1,
                "external_id": "d5889ed5-3d3f-11ef-baf5-0242ac130006",
                "name": "Category 1",
                "description": "Description 1",
                "created_at": "2022-01-01",
                "updated_at": "2022-01-01",
                "is_active": True,
            }
        )
        assert parsed_event == expected_event

    def test_when_message_is_invalid_json_then_return_none(self):
        # Test case 2: Invalid JSON data
        data = b'{"payload": {"source": {"table": "categories"}, "op": "c", "after": {"id": 1, "external_id": "d5889ed5-3d3f-11ef-baf5-0242ac130006", "name": "Category 1", "description": "Description 1", "created_at": "2022-01-01", "updated_at": "2022-01-01", "is_active": true}'
        parsed_event = parse_debezium_message(data)
        assert parsed_event is None

    def test_when_message_is_missing_required_key_then_return_none(self):
        # Test case 3: Missing key in payload
        data = b'{"payload": {}}'
        parsed_event = parse_debezium_message(data)
        assert parsed_event is None
