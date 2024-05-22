import uuid
from datetime import datetime

from elasticsearch import Elasticsearch
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

from src.api.graphql.app import graphql_app
from src.application.category.list_category import ListCategory
from src.infra.elasticsearch.category_elastic_repository import CategoryElasticRepository

app = FastAPI()
es = Elasticsearch(['http://elasticsearch:9200'])
app.include_router(graphql_app, prefix="/graphql")


class Category(BaseModel):
    id: uuid.UUID
    name: str
    description: str
    is_active: bool
    created_at: datetime


# Check if the index exists, if not, create it
if not es.indices.exists(index="categories"):
    es.indices.create(index="categories")


@app.get("/categories", response_model=list[Category])
def list_categories():
    try:
        list_use_case = ListCategory(repository=CategoryElasticRepository(es))
        output = list_use_case.execute(input=ListCategory.Input())
        return output.data
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/categories", response_model=Category)
def save_category(category: Category):  # Is it called whatsoever? Why does GraphQLController would call save?
    data = {
        "id": category.id,
        "name": category.name,
        "description": category.description,
        "is_active": category.is_active,
        "created_at": category.created_at,
        "updated_at": category.created_at,
    }
    # TODO: UseCase -> Gateway (Repository?) -> Elasticsearch
    # Index the category in Elasticsearch
    es.index(index="categories", id=str(category.id), body=data)
    return category
