from models import User
from fastapi import HTTPException
from db.db_setup import engine, User as UserDBModel
from sqlalchemy.future import select
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession
import logging


class UsersDB:
    async def get_user_by_id(self, id: int) -> User.Model:
        async with engine.connect() as session:
            try:
                stmt = select(UserDBModel).where(UserDBModel.id == id)
                result = await session.execute(stmt)
                user = result.fetchone()
                return User.Model(id=user.id, username=user.username, email=user.email, hashed_password=user.hashed_password)
            except SQLAlchemyError:
                raise HTTPException(status_code=404, detail="User not found")

    async def get_user_by_username(self, username: str) -> User.Model:
        async with engine.connect() as session:
            try:
                result = await session.execute(select(UserDBModel).where(
                    UserDBModel.username == username))
                user = result.fetchone()
                return User.Model(id=user.id, username=user.username, email=user.email, hashed_password=user.hashed_password)
            except SQLAlchemyError:
                raise HTTPException(status_code=404, detail="User not found")

    async def create_new_user(self, user: User.Model) -> User.Model:
        async with AsyncSession(engine) as session:
            try:
                new_user = UserDBModel(
                    username=user.username, email=user.email, hashed_password=user.hashed_password)
                session.add(new_user)
                await session.commit()
            except:
                await session.rollback()
                raise HTTPException(
                    status_code=400, detail="User already exists")
            return user
