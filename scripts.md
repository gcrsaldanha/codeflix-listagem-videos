```bash
# Create category
curl -X POST "http://localhost:8000/categories" \
     -H "Content-Type: application/json" \
     -d '{
           "id": "124e4567-e89b-12d3-a456-426614174000", 
           "name": "Category Name", 
           "description": "Category Description", 
           "is_active": true, 
           "created_at": "2023-01-01T00:00:00"
         }'
```


```bash
curl -X GET "http://localhost:8000/categories"
```