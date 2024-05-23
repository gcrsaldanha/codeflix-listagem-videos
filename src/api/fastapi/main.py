from contextlib import asynccontextmanager

from confluent_kafka import Consumer
from fastapi import FastAPI

from src.api.fastapi.category_router import router as category_router
from src.api.graphql.main import graphql_app
from src.infra.kafka.consumer import basic_consume_loop

# TODO: esta falhando ao tentar conectar, mesmo rodando no iPython
conf = {'bootstrap.servers': 'kafka:9092',
        'group.id': 'categories-group',
        'auto.offset.reset': 'smallest'}

consumer = Consumer(conf)
# basic_consume_loop(consumer, topics=["categories"])


@asynccontextmanager
async def lifespan(app: FastAPI):
    print("Starting Kafka Consumer...")
    # basic_consume_loop(consumer, topics=["categories"])
    yield
    print("Stopping server...")


app = FastAPI(lifespan=lifespan)
app.include_router(graphql_app, prefix="/graphql")
app.include_router(category_router, prefix="/categories")
