from motor.motor_asyncio import AsyncIOMotorClient
from pymongo.server_api import ServerApi


async def connect(uri: str) -> AsyncIOMotorClient:
    try:
        client = AsyncIOMotorClient(uri, server_api=ServerApi("1"))
        await client.admin.command("ping")
        print("Pinged your deployment. You successfully connected to MongoDB!")
        return client
    except Exception as e:
        print(e)
        raise e
