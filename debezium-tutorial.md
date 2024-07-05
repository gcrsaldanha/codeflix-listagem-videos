https://debezium.io/blog/2021/08/31/going-zookeeperless-with-debezium-container-image-for-apache-kafka/


## Setup MySQL

Docker compose:
```yaml
version: '3'
services:
  mysql:
    image: mysql:8.0
    environment:
      MYSQL_ROOT_PASSWORD: root
      MYSQL_DATABASE: codeflix
      MYSQL_USER: codeflix
      MYSQL_PASSWORD: codeflix
    volumes:
      - mysql-data:/var/lib/mysql
    ports:
      - "3306:3306"
volumes:
  mysql-data:
```

Connect to mysql:
```bash
docker compose exec -it mysql mysql --host 127.0.0.1 --port 3306 --user codeflix --password=codeflix
```

Create table
```sql
-- Step 1: Delete the existing table
DROP TABLE IF EXISTS categories;

-- Step 2: Create the new table
CREATE TABLE categories (
    id BINARY(16) DEFAULT (UUID_TO_BIN(UUID())) NOT NULL PRIMARY KEY,
    -- or
    -- id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    description TEXT,
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);

-- Step 3: Insert multiple rows
INSERT INTO categories (name, description)
VALUES
    ('Romance', 'Categoria para Romance'),
    ('Drama', 'Categoria para Drama'),
    ('Film', 'Filmes longa metragem'),
    ('Short', 'Curta-metragem');

-- Step 4: Retrieve the UUID in a readable format
SELECT
    BIN_TO_UUID(id) as id,
    name,
    description,
    is_active,
    created_at,
    updated_at
FROM categories;
```


After running connector:

curl -H "Accept:application/json" localhost:8083/
curl -H "Accept:application/json" localhost:8083/connectors/

## Register connector
Register connector to monitor database
https://debezium.io/documentation/reference/tutorial.html#registering-connector-monitor-inventory-database


- Full reference: https://debezium.io/documentation/reference/connectors/mysql.html#mysql-connector-properties

```bash
curl -i -X POST -H "Accept: application/json" -H "Content-Type: application/json" localhost:8083/connectors/ -d '{
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
```

Topics are created now!

```
# make list-topics
__consumer_offsets
catalog-db
catalog-db.codeflix.categories
my_connect_configs
my_connect_offsets
my_connect_statuses
schema-changes.catalog
```


```bash
curl -X DELETE http://localhost:8083/connectors/catalog-connector
```


```bash
curl localhost:8083/connectors/catalog-connector
```

!! User must have RELOAD permission - thus, using root.
```json
{
  "name": "catalog-connector",
  "config": {
    "connector.class": "io.debezium.connector.mysql.MySqlConnector",
    "database.user": "root",
    "topic.prefix": "catalog-db",
    "schema.history.internal.kafka.topic": "schema-changes.catalog",
    "database.server.id": "1",
    "tasks.max": "1",
    "database.hostname": "mysql",
    "database.password": "root",
    "name": "catalog-connector",
    "schema.history.internal.kafka.bootstrap.servers": "kafka:19092",
    "database.port": "3306",
    "database.include.list": "codeflix"
  },
  "tasks": [
    {
      "connector": "catalog-connector",
      "task": 0
    }
  ],
  "type": "source"
}
```


Observar Output:
```
debezium  | 2024-06-05 12:30:07,815 INFO   MySQL|catalog-db|snapshot  For table 'codeflix.categories' using select statement: 'SELECT `id`, `name`, `description`, `is_active`, `created_at` FROM `codeflix`.`categories`'   [io.debezium.relational.RelationalSnapshotChangeEventSource]
debezium  | 2024-06-05 12:30:07,829 INFO   MySQL|catalog-db|snapshot  Estimated row count for table codeflix.categories is OptionalLong[2]   [io.debezium.connector.mysql.MySqlSnapshotChangeEventSource]
debezium  | 2024-06-05 12:30:07,834 INFO   MySQL|catalog-db|snapshot  Exporting data from table 'codeflix.categories' (1 of 1 tables)   [io.debezium.relational.RelationalSnapshotChangeEventSource]
debezium  | 2024-06-05 12:30:07,849 INFO   MySQL|catalog-db|snapshot  	 Finished exporting 2 records for table 'codeflix.categories' (1 of 1 tables); total duration '00:00:00.015'   [io.debezium.relational.RelationalSnapshotChangeEventSource]
...
Snapshot ended with SnapshotResult ...
```

Indica que terminou de fazer o snapshot do banco de dados.

Verificar eventos no tópico.

```bash
docker compose exec -it kafka /opt/kafka/bin/kafka-console-consumer.sh --topic catalog-db.codeflix.categories --from-beginning --bootstrap-server localhost:9092
```

## Update table and observe changes

### Insert

```sql
INSERT INTO categories (id, name, description, is_active, created_at) VALUES
('3', 'Serie', 'Description 3', TRUE, NOW());
```

Versão simplificada:
```json
{
  "schema": {...},
  "payload": {
    "before": null,
    "after": {
      "id": "3",
      "name": "Serie",
      "description": "Description 3",
      "is_active": 1,
      "created_at": "2024-06-06T09:08:13Z"
    },
    "source": {
      "db": "codeflix",
      "table": "categories",
    }
  }
}
```

### Update

```sql
UPDATE categories SET name = 'Serie 2' WHERE id = '3';
```

```json
{
  "schema": {...},
  "payload": {
    "before": {
      "id": "3",
      "name": "Serie",
      "description": "Description 3",
      "is_active": 1,
      "created_at": "2024-06-06T09:08:13Z"
    },
    "after": {
      "id": "3",
      "name": "Serie 2",
      "description": "Description 3",
      "is_active": 1,
      "created_at": "2024-06-06T09:08:13Z"
    },
    "source": {
      "db": "codeflix",
      "table": "categories"
    }
  }
}
```

### Delete

```sql
DELETE FROM categories WHERE id = '3';
```

```json
{
  "schema": {},
  "payload": {
    "before": {
      "id": "3",
      "name": "Serie 2",
      "description": "Description 3",
      "is_active": 1,
      "created_at": "2024-06-06T09:08:13Z",
      "updated_at": "2024-06-06T09:18:33Z"
    },
    "after": null,
    "source": {
      "db": "codeflix",
      "table": "categories"
    }
  }
}
```

> ENV PYTHONUNBUFFERED=1

Esse configuração faz com que o Python não faça buffer de saída, ou seja, ele imprime na tela o log na hora.
Eu estava precisando de 2 eventos aí os dois eram impressos de uma vez.

## Consistência Eventual

Vamos parar o Kafka connector e fazer uma mudança no banco de dados. Depois iniciá-lo.
Nós não podemos garantir que os dados no nosso serviço de busca estarão sempre consistentes, mas sim, eventualmente.

> O terminal com o `consume-events` deve continuar rodando!
```
docker compose up connect
...
connect  | 2024-06-06 09:38:03,685 INFO   MySQL|catalog-db|snapshot  A previous offset indicating a completed snapshot has been found...
```

Verificar no consumer que após o connector ser inicializado, ele exibe apenas a última alteração no banco.


>  Schema changes: `make consume-events topic=schema-changes.catalog`
> MySQL mantem o registro de todas as alterações no banco de dados, incluindo as alterações de schema bn
