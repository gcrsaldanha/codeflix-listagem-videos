```sql
DROP TABLE IF EXISTS categories;
DROP TABLE IF EXISTS genres;


CREATE TABLE categories (
    id VARCHAR(36) PRIMARY KEY DEFAULT (UUID()),
    name VARCHAR(255) NOT NULL,
    description VARCHAR(255) DEFAULT '',
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);

CREATE TABLE genres (
    id VARCHAR(36) PRIMARY KEY DEFAULT (UUID()),
    name VARCHAR(255) NOT NULL,
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);


CREATE TABLE genre_categories (
    id VARCHAR(36) PRIMARY KEY DEFAULT (UUID()), -- Simple primary key to ease integration
    genre_id VARCHAR(36),
    category_id VARCHAR(36),
    FOREIGN KEY (genre_id) REFERENCES genres(id) ON DELETE CASCADE,
    FOREIGN KEY (category_id) REFERENCES categories(id) ON DELETE CASCADE
);

INSERT INTO categories (name, description)
VALUES
    ('Filme', 'Categoria para longa-metragem'),
    ('Documentary', 'Categoria para documentarios'),
    ('Curta metragem', '')
;

INSERT INTO genres (name)
VALUES
    ('Drama'),
    ('Romance')
;


DELETE FROM categories WHERE id = 'uuid';


UPDATE categories SET name = 'Serie 2' WHERE id = 'uuid';
```



```bash
# Create category
curl -X POST "http://localhost:8000/categories" \
     -H "Content-Type: application/json" \
     -d '{
           "id": "124e4567-e89b-12d3-a456-426614174000",
           "name": "Category Name",
           "description": "Category Description",
           "is_active": true,
           "created_at": "2023-01-01T00:00:00",
           "updated_at": "2023-01-01T00:00:00"
         }'

curl -X POST "http://localhost:8000/categories" \
     -H "Content-Type: application/json" \
     -d '{
           "id": "123e4567-e89b-12d3-a456-426614174000",
           "name": "Category Name",
           "description": "Category Description",
           "is_active": true,
           "created_at": "2023-01-01T00:00:00",
           "updated_at": "2023-01-01T00:00:00"
         }'



# List Categories
curl -X GET "http://localhost:8000/categories"
```


!!! Para saber que o evento foi syncado!

```
connect  | 2024-08-10 21:35:28,827 INFO   ||  4 records sent during previous 00:01:16.193, last recorded offset of {server=catalog-db} partition is {transaction_id=null, ts_sec=1723325728, file=binlog.000009, pos=6553, row=2, server_id=1, event=2}   [io.debezium.connector.common.BaseSourceTask]
```
