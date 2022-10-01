from models import User
from fastapi import HTTPException


class UsersDB:
    def __init__(self):
        self.users = []
        self.users.append(User.Model(
            id=1,
            username="umutaev",
            email="max@umutaev.ru",
            hashed_password="$2b$12$h0HEeJkRlK.J3JtnoipyQOstVLLozCjq3n4zNOE4JwCFfEA0k9kw6"
        ))

    async def get_user_by_id(self, id: int) -> User.Model:
        for user in self.users:

            if user.id == id:
                return user
        raise HTTPException(status_code=404, detail="User not found")

    async def get_user_by_username(self, username: str) -> User.Model:
        for user in self.users:
            if user.username == username:
                return user
        raise HTTPException(status_code=404, detail="User not found")

    async def create_new_user(self, user: User.Model) -> bool:
        for item in self.users:
            if item.username == user.username or item.email == user.email:
                raise HTTPException(
                    status_code=400, detail="User already exists")
        user.id = len(self.users) + 1
        self.users.append(user.copy())
        return user
