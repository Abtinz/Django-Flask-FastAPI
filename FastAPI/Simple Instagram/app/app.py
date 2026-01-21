from contextlib import asynccontextmanager
from fastapi import FastAPI, UploadFile, File, Form, Depends
from fastapi import status as HttpStatus
from app.db import create_db_and_tables, Post, get_async_session
from sqlalchemy import text, select
from sqlalchemy.ext.asyncio import AsyncSession
from app.schemas import PostResponse
from app.imagekit_manager import ImageKitHandler
from app.users_manager import fastapi_users, current_active_user, auth_backend

@asynccontextmanager
async def lifespan(app: FastAPI):
    '''Lifespan context manager to create database tables on startup.'''
    await create_db_and_tables()
    yield

app = FastAPI(lifespan=lifespan)

app.include_router(
    fastapi_users.get_auth_router(auth_backend), prefix="/auth/jwt", tags=["auth"]
)
app.include_router(
    fastapi_users.get_register_router(), prefix="/auth", tags=["auth"]
)
app.include_router(
    fastapi_users.get_users_router(), prefix="/users", tags=["users"]
)       
app.include_router( 
    fastapi_users.get_reset_password_router(), prefix="/auth", tags=["auth"]
)
app.include_router(
    fastapi_users.get_verify_router(), prefix="/auth", tags=["auth"]
) 

@app.post("/upload")
async def upload_file(
    file: UploadFile = File(...),
    caption: str = Form(""),
    session: AsyncSession = Depends(get_async_session)
):

    imagekit_result = ImageKitHandler().upload_image(file)
    print("ImageKit upload result:", imagekit_result)

    post = Post(
        caption=caption,
        url=imagekit_result['response']['url'],
        file_type=imagekit_result['response']['fileType'],
        file_name=imagekit_result['response']['name']
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

@app.delete("/posts/{post_id}")
async def delete_post(post_id: str, session: AsyncSession = Depends(get_async_session)):
    '''Delete a post by its ID.
    
    Args:
        post_id (str): The ID of the post to delete.
        session (AsyncSession): The database session.
    Returns:
            dict: A message indicating the result of the deletion.
    '''

    result = await session.execute(select(Post).where(Post.id == post_id))
    post = result.scalar_one_or_none()
    if post is None:
        return {
            "error": "Post not found",
            "code": HttpStatus.HTTP_404_NOT_FOUND
        }

    await session.delete(post)
    await session.commit()
    return {
        "message": "Post deleted successfully"
    }

