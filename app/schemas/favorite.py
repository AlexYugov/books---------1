from pydantic import BaseModel
from .book import BookSchema

class FavoriteCreate(BaseModel):
    book_id: int

class FavoriteSchema(BaseModel):
    id: int
    user_id: int
    book_id: int
    book: BookSchema | None

    class Config:
        from_attributes = True