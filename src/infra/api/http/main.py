import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI

from src.config import ENABLE_GRAPHQL
from src.infra.api.http.category_router import router as category_router

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("Starting server")
    yield
    logger.info("Stopping server")


app = FastAPI(lifespan=lifespan)
app.include_router(category_router, prefix="/categories")

if ENABLE_GRAPHQL:
    from src.infra.api.graphql.main import graphql_app

    app.include_router(graphql_app, prefix="/graphql")
