from contextlib import asynccontextmanager
from fastapi import FastAPI, UploadFile, File, Form, Depends
from app.db import create_db_and_tables, Post, get_async_session
from sqlalchemy import text, select
from sqlalchemy.ext.asyncio import AsyncSession
from app.schemas import PostResponse

@asynccontextmanager
async def lifespan(app: FastAPI):
    '''Lifespan context manager to create database tables on startup.'''
    await create_db_and_tables()
    yield

app = FastAPI(lifespan=lifespan)

@app.post("/upload")
async def upload_file(
    file: UploadFile = File(...),
    caption: str = Form(""),
    session: AsyncSession = Depends(get_async_session)
):
    post = Post(
        caption=caption,
        url="dummy url",
        file_type="photo",
        file_name="dummy name"
    )

    session.add(post)
    await session.commit()
    print("post before refresh:", post)
    await session.refresh(post) 
    print("post after refresh:", post)
    return post

@app.get("/posts/", response_model=list[PostResponse])
async def get_posts(session: AsyncSession = Depends(get_async_session)):
    result = await session.execute(select(Post))
    posts = result.scalars().all()
    return posts