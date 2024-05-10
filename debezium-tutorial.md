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
CREATE TABLE categories (
    id CHAR(36) PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    description TEXT,
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

Insert records
```sql
INSERT INTO categories (id, name, description, is_active, created_at) VALUES
('1', 'Film', 'Description 1', TRUE, NOW()),
('2', 'Documentary', 'Description 2', TRUE, NOW());
```
