import strawberry

from app.models.user_model import User, UserType, CreateUserInput


@strawberry.type
class UserMutation:
    @strawberry.mutation
    def login(self, input: CreateUserInput) -> UserType | None:
        try:
            user = User(id="1", name=input.name)
            # info.context["background_tasks"].add_task(send_email, input.name)
            return UserType.from_pydantic(user)
        except Exception as e:
            print(e)
            return None
