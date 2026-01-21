from pydantic import BaseModel
from datetime import datetime
from uuid import UUID
from fastapi_users import schemas

class PostCreate(BaseModel):
    '''Schema for creating a new post'''
    title: str
    content: str

class PostResponse(BaseModel):
    '''Schema for returning a post'''
    id: UUID
    caption: str
    url: str
    file_type: str
    file_name: str
    created_at: datetime
    user_id: UUID
    user: UserResponse

    class Config:
        from_attributes = True

class UserRead(schemas.BaseUser[UUID]):
    '''Schema for reading user information'''
    pass

class UserCreate(schemas.BaseUserCreate):
    '''Schema for creating a new user'''
    pass    

class UserUpdate(schemas.BaseUserUpdate):
    '''Schema for updating user information'''
    pass 

class UserResponse(BaseModel):
    '''Schema for returning user information'''
    id: UUID
    email: str
    is_active: bool
    is_superuser: bool
    is_verified: bool

    class Config:
        from_attributes = True