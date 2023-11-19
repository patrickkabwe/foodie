import strawberry

from app.graphql_api.mutations import user_mutation
from app.graphql_api.queries import user_query


@strawberry.type
class RootQuery(user_query.UserQuery):
    pass


@strawberry.type
class RootMutation(user_mutation.UserMutation):
    pass


schema = strawberry.Schema(query=RootQuery, mutation=RootMutation)
