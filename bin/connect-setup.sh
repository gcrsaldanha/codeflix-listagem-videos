#!/bin/sh
echo "Kafka Connect started. Registering Debezium connector..."

printf "Registering Debezium connector...\n"
curl -i -X POST -H "Accept: application/json" -H "Content-Type: application/json" connect:8083/connectors/ -d '{
  "name": "catalog-connector",
  "config": {
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
  }
}'
printf "Debezium connector registered.\n\n"


printf "Registering Elasticsearch Sink connector...\n"
curl -X POST -H "Accept: application/json" -H "Content-Type: application/json" http://connect:8083/connectors/ -d '{
  "name": "elasticsearch-sink-connector",
  "config": {
    "connector.class": "io.confluent.connect.elasticsearch.ElasticsearchSinkConnector",
    "tasks.max": "1",
    "topics.regex": "catalog-db\\.codeflix\\..*",
    "connection.url": "http://elasticsearch:9200",
    "transforms": "unwrap,key",
    "transforms.unwrap.type": "io.debezium.transforms.ExtractNewRecordState",
    "transforms.key.type": "org.apache.kafka.connect.transforms.ExtractField$Key",
    "transforms.key.field": "id",
    "key.ignore": "false",
    "behavior.on.null.values": "delete"
  }
}'
printf "Elasticsearch Sink connector registered.\n\n"
