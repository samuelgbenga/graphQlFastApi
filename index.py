import strawberry
from fastapi import FastAPI
from strawberry.fastapi import GraphQLRouter
from typing import List, Optional

app = FastAPI()

# In-memory "database"
users_db = {}
current_id = 1

@strawberry.type
class User:
    id: int
    name: str
    email: str

@strawberry.type
class Query:
    @strawberry.field
    def get_user(self, id: int) -> Optional[User]:
        return users_db.get(id)

    @strawberry.field
    def get_all_users(self) -> List[User]:
        return list(users_db.values())

@strawberry.type
class Mutation:
    @strawberry.mutation
    def create_user(self, name: str, email: str) -> User:
        global current_id
        new_user = User(id=current_id, name=name, email=email)
        users_db[current_id] = new_user
        current_id += 1
        return new_user

    @strawberry.mutation
    def update_user(self, id: int, name: Optional[str] = None, email: Optional[str] = None) -> Optional[User]:
        user = users_db.get(id)
        if not user:
            return None
        if name:
            user.name = name
        if email:
            user.email = email
        return user

    @strawberry.mutation
    def delete_user(self, id: int) -> bool:
        if id in users_db:
            del users_db[id]
            return True
        return False

schema = strawberry.Schema(query=Query, mutation=Mutation)
graphql_app = GraphQLRouter(schema)

app.include_router(graphql_app, prefix="/graphql")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
