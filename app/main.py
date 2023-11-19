from contextlib import asynccontextmanager

from fastapi import FastAPI, Depends
from strawberry.fastapi import GraphQLRouter

from app.graphql_api.schema import schema
from app.services import user_service
from database import db


def custom_context_dependency() -> str:
    return "John"


async def get_context(
    custom_value=Depends(custom_context_dependency),
):
    return {
        "custom_value": custom_value,
        "services": {
            "user_service": user_service.UserService(),
        },
    }


graphql_app = GraphQLRouter(schema=schema, context_getter=get_context)


@asynccontextmanager
async def lifespan(_: FastAPI):
    client: db.AsyncIOMotorClient = None
    try:
        client = await db.connect("mongodb://localhost:27017/foodie")
        yield
    finally:
        await client.close()
        print("Disconnected from MongoDB!")


app = FastAPI(lifespan=lifespan)


app.include_router(graphql_app, prefix="/graphql")

if __name__ == "__main__":
    import uvicorn

    uvicorn.run("main:app", host="0.0.0.0", reload=True)
