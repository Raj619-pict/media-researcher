from pydantic import BaseModel

class PostBase(BaseModel):
    title: str
    content: str
    class Config:
        orm_mode = True

class CreatePost(PostBase):
    pass
