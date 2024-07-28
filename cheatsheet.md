```sql
DROP TABLE IF EXISTS categories;


CREATE TABLE categories (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    description TEXT,
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);


INSERT INTO categories (name, description)
VALUES
    ('Romance', 'Categoria para Romance'),
    ('Drama', 'Categoria para Drama'),
    ('Film', 'Filmes longa metragem'),
    ('Short', 'Curta-metragem');


DELETE FROM categories WHERE id = '3';


UPDATE categories SET name = 'Serie 2' WHERE id = '3';
```
