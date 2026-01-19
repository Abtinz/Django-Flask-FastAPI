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
    pass

class Post(Base):
    '''SQLAlchemy model for a Post 
    Attributes:
        id (UUID): Primary key for the post.
        user_id (UUID): Foreign key referencing the user who created the post.
        caption (Text): Caption for the post.
        url (String): URL of the post's media.
        file_type (String): Type of the media file (e.g., image, video).
        file_name (String): Name of the media file.
        created_at (DateTime): Timestamp when the post was created.
    '''
    __tablename__ = "posts"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    #user_id = Column(UUID(as_uuid=True), ForeignKey("user.id"), nullable=False)
    caption = Column(Text)
    url = Column(String, nullable=False)
    file_type = Column(String, nullable=False)
    file_name = Column(String, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)


engine = create_async_engine(DATABASE_URL, echo=True)
async_session_maker = async_sessionmaker(engine, expire_on_commit=False)



async def create_db_and_tables():
    '''Create database tables based on the defined models.'''
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


async def get_async_session() -> AsyncGenerator[AsyncSession, None]:
    '''Dependency that provides an asynchronous database session.'''
    async with async_session_maker() as session:
        yield session