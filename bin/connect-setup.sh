#!/bin/sh
echo "Kafka Connect started. Registering Debezium connector..."

# Register the Debezium connector
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
