.PHONY: run-kafka create-topic produce-events consume-events run-connect shell-kafka

run-kafka:
	docker compose up -d kafka

create-topic:
	docker compose exec -it kafka /opt/kafka/bin/kafka-topics.sh --create --topic categories --bootstrap-server localhost:9092

produce-events:
	docker compose exec -it kafka /opt/kafka/bin/kafka-console-producer.sh --topic categories --bootstrap-server localhost:9092

consume-events:
	docker compose exec -it kafka /opt/kafka/bin/kafka-console-consumer.sh --topic categories --from-beginning --bootstrap-server localhost:9092

run-connect:
	docker compose exec -it kafka \
	/opt/kafka/bin/connect-standalone.sh \
	/opt/kafka/config/connect-standalone.properties \
	/opt/kafka/config/connect-file-source.properties \
	/opt/kafka/config/connect-file-sink.properties

shell-kafka:
	docker compose exec kafka bash

mysql:
	docker compose exec -it mysql mysql --host 127.0.0.1 --port 3306 --user codeflix --password=codeflix

build:
	docker compose build
