from collections.abc import AsyncGenerator
from sqlalchemy import Column, String, Text, DateTime, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker
from sqlalchemy.orm import DeclarativeBase, relationship
from datetime import datetime
from fastapi_users.db import SQLAlchemyUserDatabase, SQLAlchemyBaseUserTableUUID
from fastapi import Depends
import uuid

DATABASE_URL = "sqlite+aiosqlite:///./test.db"

class Base(DeclarativeBase):
    '''DeclarativeBase

    It's a base class that our own model classes inherit from.
    When our models (like User and Post) inherit from a class that is a DeclarativeBase, 
    SQLAlchemy can automatically discover them and map them to database tables.
    '''
    pass

""" SQLAlchemyBaseUserTableUUID
    Base class for User model with UUID primary key.
    It defines columns like id (as a UUID), email, hashed_password,
    is_active, is_superuser, and is_verified.
"""
class User(SQLAlchemyBaseUserTableUUID, Base):
    '''User model extending FastAPI Users base user table with UUID primary key.'''
    posts = relationship("Post", back_populates="user")

class Post(Base):
    __tablename__ = "posts"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    caption = Column(Text)
    url = Column(String, nullable=False)
    file_type = Column(String, nullable=False)
    file_name = Column(String, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    # User relationship is been defined here
    user = relationship("User", back_populates="posts")
    user_id = Column(UUID(as_uuid=True), ForeignKey("user.id"), nullable=False)

# Create the central connection interface to your database.
engine = create_async_engine(DATABASE_URL, echo=True)
async_session_maker = async_sessionmaker(engine, expire_on_commit=False)


async def create_db_and_tables():
    '''Create database tables based on the defined models.
    
    This function initializes the database by creating all tables
    defined in the SQLAlchemy models.
    '''
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


async def get_async_session() -> AsyncGenerator[AsyncSession, None]:
    '''Dependency that provides an asynchronous database session.
    
    Yields:
        AsyncSession: The asynchronous database session.
    '''
    async with async_session_maker() as session:
        yield session

async def get_user_db(session: AsyncSession = Depends(get_async_session)):
    '''Dependency that provides a user database interface for FastAPI Users.
    
    Args:
        session (AsyncSession): The asynchronous database session.
        
    Yields:
            SQLAlchemyUserDatabase: The user database interface.
    '''
    yield SQLAlchemyUserDatabase(session, User)