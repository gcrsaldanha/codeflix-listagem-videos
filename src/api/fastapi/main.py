import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI

from src.api.fastapi.category_router import router as category_router
from src.api.graphql.main import graphql_app

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("Starting server")
    yield
    logger.info("Stopping server")


app = FastAPI(lifespan=lifespan)
app.include_router(graphql_app, prefix="/graphql")
app.include_router(category_router, prefix="/categories")
