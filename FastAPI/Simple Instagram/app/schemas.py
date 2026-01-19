from pydantic import BaseModel
from datetime import datetime
from uuid import UUID

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

    class Config:
        from_attributes = True