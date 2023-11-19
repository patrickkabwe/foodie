from typing import Any, Mapping, Union

import bson
from motor.motor_asyncio import (
    AsyncIOMotorDatabase,
    AsyncIOMotorClient,
    AsyncIOMotorCursor,
)
from pymongo.operations import _Pipeline
from pymongo.results import InsertOneResult, UpdateResult, DeleteResult


class UserRepository:
    db: AsyncIOMotorClient = None
    collection = "users"

    def __init__(self, _db: AsyncIOMotorDatabase):
        self.db = _db

    async def find_by_id(self, user_id: bson.ObjectId) -> dict:
        return await self.db[self.collection].find_one({"_id": user_id})

    async def find_all(self, filters: dict) -> AsyncIOMotorCursor:
        users = self.db[self.collection].find(filters)
        return await users.to_list(filters.get("limit", 100))

    async def create(self, user: dict) -> InsertOneResult:
        return await self.db[self.collection].insert_one(user)

    async def find_and_update(self, filters: dict, user: dict):
        return await self.db[self.collection].find_one_and_update(filters, user)

    async def update(
        self,
        filters: Mapping[str, Any],
        user: Union[Mapping[str, Any], _Pipeline],
    ) -> UpdateResult:
        return await self.db[self.collection].update_one(
            filters,
            user,
        )

    async def delete(self, filters: dict) -> DeleteResult:
        return await self.db[self.collection].delete_one(filters)
