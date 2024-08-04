```sql
DROP TABLE IF EXISTS categories;
DROP TABLE IF EXISTS genres;


CREATE TABLE categories (
    id VARCHAR(36) PRIMARY KEY DEFAULT (UUID()),
    name VARCHAR(255) NOT NULL,
    description TEXT,
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
    FOREIGN KEY (category_id) REFERENCES categories(id) ON DELETE CASCADE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

INSERT INTO categories (name, description)
VALUES
    ('Filme', 'Categoria para longa-metragem'),
    ('Documentary', 'Categoria para documentarios')
;

INSERT INTO genres (name)
VALUES
    ('Drama')
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
