curl -X PUT "http://localhost:9200/_template/uuid_template" -H "Content-Type: application/json" -d'
{
  "index_patterns": ["your-index-*"],
  "settings": {
    "number_of_shards": 1
  },
  "mappings": {
    "properties": {
      "id": {
        "type": "keyword"
      }
    }
  }
}'
