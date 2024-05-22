from fastapi import FastAPI, HTTPException, Body
from elasticsearch import Elasticsearch
from pydantic import BaseModel
import uuid

app = FastAPI()
es = Elasticsearch(['http://elasticsearch:9200'])


class Category(BaseModel):
    name: str
    description: str
    is_active: bool


# Check if the index exists, if not, create it
if not es.indices.exists(index="categories"):
    es.indices.create(index="categories")

@app.post("/categories", response_model=Category)
def save_category(category: Category):
    category_id = str(uuid.uuid4())
    data = {
        "id": category_id,
        "name": category.name,
        "description": category.description,
        "is_active": category.is_active,
        "created_at": "now"
    }
    # Index the category in Elasticsearch
    es.index(index="categories", id=category_id, body=data)
    return category

@app.get("/categories", response_model=list[Category])
def get_categories():
    try:
        result = es.search(index="categories", body={"query": {"match_all": {}}})
        categories = [hit["_source"] for hit in result["hits"]["hits"]]
        return categories
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
