import strawberry

from app.models.user_model import UserType


@strawberry.type(
    description="The User type represents a user in the system",
)
class UserQuery:
    @strawberry.field(
        description="Returns 'User' when called",
    )
    def user(self) -> UserType:
        return UserType(id="1", name="User")
