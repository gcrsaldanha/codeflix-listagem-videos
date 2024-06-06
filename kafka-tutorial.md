https://github.com/provectus/kafka-ui
https://kafka.apache.org/quickstart

What is Apache Kafka
https://www.youtube.com/watch?v=06iRM1Ghr1k
- Traditional storage vs Kafka (event storing/streaming)
- Topics: separação de eventos por tópicos (interessados)
- Serviços consomem/produzem eventos de/para um tópico
- Kafka pode se integrar à outros sistemas utilizando Connectors (Kafka Connect)
  - Por exemplo: Debezium MySQL Connector
  - Coletar mudanças em um banco de dados para tópicos do Kafka.
  - Input **e** output (de/para outros sistemas).
  - Kafka connect é uma interface para plugin esses connectors.
- Kafka services:
  - Grouping, aggregating, filtering, enriching messages.
  - Kafka Streams: Java API para processamento de eventos em tempo real.
  - KSQL: SQL-like language para processamento de eventos em tempo real.
    - Caso eu não queira rodar um programa Java para processar eventos.
- events === messages === records
- [Events](https://kafka.apache.org/documentation/#messages)
- [Topics](https://kafka.apache.org/documentation/#intro_concepts_and_terms)

## Step 1: Baixar e rodar Kafka
```bash
docker pull apache/kafka:3.7.0
docker run -p 9092:9092 apache/kafka:3.7.0
```

## Step 2: Criar um tópico
Precisamos de tópicos para poder organizar/armazenar os eventos. Análogos a pastas no sistema de arquivos.

```bash
docker exec -it <container_id/name> /opt/kafka/bin/kafka-topics.sh --create --topic my-topic --bootstrap-server localhost:9092
docker exec -it relaxed_poitras /opt/kafka/bin/kafka-topics.sh --create --topic my-topic --bootstrap-server localhost:9092
# Created topic my-topic.
#$ bin/kafka-topics.sh --create --topic quickstart-events --bootstrap-server localhost:9092
```

> --bootstrap-server: endereço do servidor ("broker") Kafka. No caso, localhost:9092. Todo cliente (producer, consumer, etc) precisa de um broker para se conectar.


## Step 3: Produzir eventos
Vamos produzir eventos para o tópico criado.

```bash
docker exec -it relaxed_poitras /opt/kafka/bin/kafka-console-producer.sh --topic my-topic --bootstrap-server localhost:9092
#> Hello, Kafka 1!
#> Hello, Kafka 2!
#> Hello, Kafka 3!
```


## Step 4:  Ler eventos
Vamos ler os eventos que produzimos.

```bash
docker exec -it relaxed_poitras /opt/kafka/bin/kafka-console-consumer.sh --topic my-topic --from-beginning --bootstrap-server localhost:9092
#> Hello, Kafka 1!
#> Hello, Kafka 2!
#> Hello, Kafka 3!
```


## Step 5: Produzir e Ler eventos simultaneamente
Executar passos 4 e 5 em terminais diferentes.

> Eventos Kafka são **duráveis**. Eles são armazenados em disco e podem ser lidos várias vezes.
> No nosso caso, temos que tomar cuidado porque se deletarmos o docker container que está rodando o Kafka, os eventos serão perdidos.
> Vamos resolver isso com um volume depois.


## Step 6: Importar/Exportar dados com Kafka Connect
- [Kafka Connect docs](https://kafka.apache.org/documentation/#connect)
- [plugin path](https://kafka.apache.org/documentation/#connectconfigs_plugin.path)
- Existem vários connectors disponíveis. Como exemploa agora, vamos só utilizar um que lê/escreve em um arquivo.
- Configurar os arquivos
  - `/opt/kafka/config/connect-standalone.properties`: plugin.path=/opt/kafka/libs/connect-file-3.7.0.jar, 
  - `/opt/kafka/config/connect-file-source.properties`: file=/opt/kafka/data/test.txt and topic
  - `/opt/kafka/config/connect-file-sink.properties`: file=/opt/kafka/data/test.sink.txt and topic
 
```bash
docker exec -it relaxed_poitras \
/opt/kafka/bin/connect-standalone.sh \
/opt/kafka/config/connect-standalone.properties \
/opt/kafka/config/connect-file-source.properties \
/opt/kafka/config/connect-file-sink.properties
```

- Adicionar dados ao arquivo `test.txt` e ver o que acontece. (echo "qasdfasdf" >> test.txt, tail -f text.sink.txt)
- Também conseguimos verificar as mensagens no topic `connect-test`!

```bash
docker exec -it relaxed_poitras /opt/kafka/bin/kafka-console-consumer.sh --topic connect-test --from-beginning --bootstrap-server localhost:9092
```

> Qualquer texto adicionado ao `test.txt` será replicado no `test.sink.txt` e no console.

- [] Fazer diagrama.

## Step 7: Processando eventos com Kafka Streams [skip]

Kafka Stream é uma biblioteca em Java para processamento de eventos em tempo real.

Ela permite a execução de **consultas** (SQL-like) em streams de eventos.

Por exemplo, podemos escrever uma aplicação em java, e executá-la em cima do nosso stream de eventos (ETL). Não vamos fazer isso agora.

```
```

## Step 8: Criar docker volume para persistência de dados
```bash
docker volume create kafka-data
docker run -p 9092:9092 -v kafka-data:/var/lib/kafka apache/kafka:3.7.0
```

### Docker compose
From the official docker image:
https://github.com/apache/kafka/blob/trunk/docker/examples/README.md


### Por que não consigo conectar no container?

https://www.confluent.io/blog/kafka-listeners-explained/

```yaml
version: '3'
services:
  kafka:
    image: apache/kafka:3.7.0
    ports:
      - "9092:9092"
    volumes:
      - kafka-data:/var/lib/kafka
volumes:
    kafka-data:
```


### Partitioning

- Dividir um topic em varias partições. Se a mensagem não tem uma `key`, kafka faz round robin.
- Podemos utilizar a `key` como o `id` da entidade, assim garantimos que as mensagens relacionadas a uma entidade vão para a mesma partição, logo, vão ser processadas na ordem correta.
