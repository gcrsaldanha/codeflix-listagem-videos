```bash
# Create category
curl -X POST "http://localhost:8000/categories" -H "Content-Type: application/json" -d '{"name": "Category Name", "description": "Category Description", "is_active": true}'
```

```bash
curl -X GET "http://localhost:8000/categories"
```
