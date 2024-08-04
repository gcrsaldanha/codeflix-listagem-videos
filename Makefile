.PHONY: run-kafka create-topic produce-events consume-events run-connect shell-kafka

run-kafka:
	docker compose up -d kafka

create-topic:
	docker compose exec -it kafka /opt/kafka/bin/kafka-topics.sh --create --topic $(topic) --bootstrap-server localhost:9092

list-topics:
	docker compose exec -it kafka /opt/kafka/bin/kafka-topics.sh --list --bootstrap-server localhost:9092

delete-topic:
	docker compose exec -it kafka /opt/kafka/bin/kafka-topics.sh --delete --topic $(topic) --bootstrap-server localhost:9092

produce-events:
	docker compose exec -it kafka /opt/kafka/bin/kafka-console-producer.sh --topic $(topic) --bootstrap-server localhost:9092

consume-events:
	docker compose exec -it kafka /opt/kafka/bin/kafka-console-consumer.sh --topic $(topic) --from-beginning --bootstrap-server localhost:9092

run-consumer:
	docker compose up -d consumer

list-connectors:
	curl localhost:8083/connectors/

delete-connector:
	curl -X DELETE localhost:8083/connectors/$(connector)


run-connect:
	docker compose exec -it kafka \
	/opt/kafka/bin/connect-standalone.sh \
	/opt/kafka/config/connect-standalone.properties \
	/opt/kafka/config/connect-file-source.properties \
	/opt/kafka/config/connect-file-sink.properties

shell-kafka:
	docker compose exec kafka bash

mysql:
	docker compose exec -it mysql mysql --host 127.0.0.1 --port 3306 --user codeflix --password=codeflix --database=codeflix

build:
	docker compose build

test:
	docker compose run --rm integration-tests

unit:
	docker compose run --rm unit-tests
