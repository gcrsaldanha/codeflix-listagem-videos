#!/bin/sh
curl -X DELETE -H "Accept: application/json" -H "Content-Type: application/json" http://connect:8083/connectors/debezium-cdc/

curl -X DELETE -H "Accept: application/json" -H "Content-Type: application/json" http://connect:8083/connectors/elastic-sink/
