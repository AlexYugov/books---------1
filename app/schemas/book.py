from pydantic import BaseModel
from typing import Optional

class BookCreate(BaseModel):
    title: str
    author: str
    genre: str
    year: int
    condition: str
    city: str
    cover_image: str
    contacts: Optional[str] = None  # Добавлено поле для контактов

class BookUpdate(BaseModel):
    title: Optional[str] = None
    author: Optional[str] = None
    genre: Optional[str] = None
    year: Optional[int] = None
    condition: Optional[str] = None
    city: Optional[str] = None
    cover_image: Optional[str] = None
    contacts: Optional[str] = None  # Добавлено поле для контактов

class BookSchema(BaseModel):
    id: int
    title: str
    author: str
    genre: str
    year: int
    condition: str
    city: str
    cover_image: str
    contacts: Optional[str] = None  # Добавлено поле для контактов
    owner_id: int
    status: str
    owner_login: Optional[str] = None

    class Config:
        from_attributes = True