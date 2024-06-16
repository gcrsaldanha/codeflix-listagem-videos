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
```

```bash
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
```



```bash
curl -X GET "http://localhost:8000/categories"
```


curl -X POST "http://localhost:8000/categories/" \
     -H "Content-Type: application/json" \
     -d '{
           "id": "125e4567-e89b-12d3-a456-426614174000", 
           "name": "Dramaaa", 
           "description": "Description for drama", 
           "is_active": true, 
           "created_at": "2023-01-01T00:00:00",
           "updated_at": "2023-01-01T00:00:00"
         }'
