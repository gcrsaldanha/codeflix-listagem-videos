#!/bin/sh
curl -X PUT -H "Accept: application/json" -H "Content-Type: application/json" http://connect:8083/connectors/elastic-sink/config/ -d '{
        "connector.class": "io.confluent.connect.elasticsearch.ElasticsearchSinkConnector",
        "tasks.max": "1",
        "topics": "catalog-db.codeflix.categories,catalog-db.codeflix.genres",
        "connection.url": "http://elasticsearch:9200",
        "transforms": "unwrap,key",
        "transforms.unwrap.type": "io.debezium.transforms.ExtractNewRecordState",
        "transforms.unwrap.drop.tombstones": "false",
        "transforms.unwrap.drop.deletes": "false",
        "behavior.on.null.values": "delete",
        "transforms.key.type": "org.apache.kafka.connect.transforms.ExtractField$Key",
        "transforms.key.field": "id",
        "key.ignore": "false"
    }'

curl -X PUT -H "Accept: application/json" -H "Content-Type: application/json" http://connect:8083/connectors/debezium-cdc/config/ -d '{
    "connector.class": "io.debezium.connector.mysql.MySqlConnector",
    "tasks.max": "1",
    "database.hostname": "mysql",
    "database.port": "3306",
    "database.user": "root",
    "database.password": "root",
    "database.server.id": "1",
    "topic.prefix": "catalog-db",
    "database.include.list": "codeflix",
    "schema.history.internal.kafka.bootstrap.servers": "kafka:19092",
    "schema.history.internal.kafka.topic": "schema-changes.catalog"
}'
