from pydantic import BaseModel

class CommentCreate(BaseModel):
    content: str

class CommentUpdate(BaseModel):
    content: str

class CommentSchema(CommentCreate):
    id: int
    user_id: int
    book_id: int
    username: str

    class Config:
        from_attributes = True