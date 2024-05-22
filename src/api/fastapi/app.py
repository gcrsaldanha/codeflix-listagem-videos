import uuid
from datetime import datetime

from elasticsearch import Elasticsearch
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI()
es = Elasticsearch(['http://elasticsearch:9200'])


class Category(BaseModel):
    id: uuid.UUID
    name: str
    description: str
    is_active: bool
    created_at: datetime


# Check if the index exists, if not, create it
if not es.indices.exists(index="categories"):
    es.indices.create(index="categories")


@app.post("/categories", response_model=Category)
def save_category(category: Category):  # Called from Kafka Consumer
    data = {
        "id": category.id,
        "name": category.name,
        "description": category.description,
        "is_active": category.is_active,
        "created_at": category.created_at
    }
    # TODO: UseCase -> Gateway (Repository?) -> Elasticsearch
    # Index the category in Elasticsearch
    es.index(index="categories", id=str(category.id), body=data)
    return category


@app.get("/categories", response_model=list[Category])
def list_categories():
    try:
        result = es.search(index="categories", body={"query": {"match_all": {}}})
        categories = [hit["_source"] for hit in result["hits"]["hits"]]
        return categories
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
