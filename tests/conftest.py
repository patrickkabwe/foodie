import pytest

from database.db import connect


@pytest.fixture
async def db():
    """Returns an instance of the database."""
    client = await connect("mongodb://localhost:27017/foodie-test")
    await client.drop_database("foodie-test")
    return client["foodie-test"]
