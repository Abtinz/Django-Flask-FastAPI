from pydantic import BaseModel

class PostCreate(BaseModel):
    '''Schema for creating a new post'''
    title: str
    content: str