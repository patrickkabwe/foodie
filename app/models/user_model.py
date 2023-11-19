import strawberry
from pydantic import BaseModel


class User(BaseModel):
    id: str
    name: str


@strawberry.experimental.pydantic.input(model=User)
class CreateUserInput:
    name: strawberry.auto


@strawberry.experimental.pydantic.type(model=User)
class UserType:
    id: strawberry.auto
    name: strawberry.auto
