https://www.elastic.co/blog/getting-started-with-the-elastic-stack-and-docker-compose


```bash
docker pull docker.elastic.co/elasticsearch/elasticsearch:8.13.4
export ELASTIC_PASSWORD="123456"  # From docker run command
docker run --name es01 --net codeflix-listagem-videos_default -p 9200:9200 -p 9300:9300 -e "discovery.type=single-node" -e ELASTIC_PASSWORD=$ELASTIC_PASSWORD -t docker.elastic.co/elasticsearch/elasticsearch:8.13.4
docker cp es01:/usr/share/elasticsearch/config/certs/http_ca.crt .
curl --cacert http_ca.crt -u elastic:$ELASTIC_PASSWORD https://localhost:9200
docker pull docker.elastic.co/kibana/kibana:8.13.4
docker run --name kibana --net codeflix-listagem-videos_default -p 5601:5601 docker.elastic.co/kibana/kibana:8.13.4
```
