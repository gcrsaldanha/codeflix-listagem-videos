#!/bin/sh
curl -X DELETE -H "Accept: application/json" -H "Content-Type: application/json" http://connect:8083/connectors/elasticsearch-sink-connector/

curl -X DELETE -H "Accept: application/json" -H "Content-Type: application/json" http://connect:8083/connectors/catalog-db-connector/
