from fastapi import FastAPI

from src.api.fastapi.category_router import router as category_router
from src.api.graphql.main import graphql_app

app = FastAPI()
app.include_router(graphql_app, prefix="/graphql")
app.include_router(category_router, prefix="/categories")
