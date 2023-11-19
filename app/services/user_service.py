import bson

from app.models.user_model import User
from app.repositories.user_repository import UserRepository


class UserService:
    user_repository: UserRepository = None

    def __init__(self, user_repository: UserRepository):
        self.user_repository = user_repository

    async def create_user(self, name: str) -> User:
        user = await self.user_repository.create({"name": name})
        return User(id=str(user.inserted_id), name=name)

    async def update_user(self, _id: str, name: str) -> User | None:
        try:
            bson_id = bson.ObjectId(_id)
            result = await self.user_repository.update(
                filters={"_id": bson_id}, user={"$set": {"name": name}}
            )
            user = await self.get_user(_id=result.upserted_id)
            return user
        except bson.errors.InvalidId:
            raise ValueError("Invalid id")

    async def delete_user(self, _id: str) -> dict | None:
        try:
            bson_id = bson.ObjectId(_id)
            result = await self.user_repository.delete(filters={"_id": bson_id})
            if result.deleted_count == 0:
                return None
            return {"id": _id}
        except bson.errors.InvalidId:
            raise ValueError("Invalid id")

    async def get_user(self, _id: str) -> User | None:
        try:
            bson_id = bson.ObjectId(_id)
            user = await self.user_repository.find_by_id(user_id=bson_id)
            if user is None:
                return None
            return User(id=str(user["_id"]), name=user["name"])
        except bson.errors.InvalidId:
            raise ValueError("Invalid id")

    async def get_all_users(self) -> list[User]:
        users = await self.user_repository.find_all({})
        return [User(id=str(user["_id"]), name=user["name"]) for user in users]
