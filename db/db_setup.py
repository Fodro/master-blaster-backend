from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.orm import declarative_base, relationship
import os
import asyncio

Base = declarative_base()

DB_LINK = str(os.environ['DB_LINK'])

engine = create_async_engine(DB_LINK)


class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    username = Column(String, unique=True, nullable=False)
    email = Column(String, unique=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    projects = relationship("Project")


class Project(Base):
    __tablename__ = 'project'
    id = Column(Integer, primary_key=True)
    file_link = Column(String, unique=True)
    creation_date = Column(DateTime, nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"))


async def setup():
    engine = create_async_engine(DB_LINK)
    async with engine.begin() as conn:
        # await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)
