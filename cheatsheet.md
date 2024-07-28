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

CREATE TABLE genres (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
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


DELETE FROM categories WHERE id = '3';


UPDATE categories SET name = 'Serie 2' WHERE id = '3';
```


```bash

```
