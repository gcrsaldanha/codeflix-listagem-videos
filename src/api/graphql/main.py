from strawberry.fastapi import GraphQLRouter

from src.api.graphql.schemas import schema

graphql_app = GraphQLRouter(schema)

# Run: strawberry server src.api.graphql.app.schema --port 8001
