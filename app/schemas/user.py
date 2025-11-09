from pydantic import BaseModel, EmailStr
from typing import Optional

class UserCreate(BaseModel):
    login: str
    email: EmailStr
    city: str
    password: str

class UserUpdate(BaseModel):
    login: Optional[str] = None
    email: Optional[EmailStr] = None
    city: Optional[str] = None
    password: Optional[str] = None

class UserSchema(BaseModel):
    id: int
    login: str
    email: EmailStr
    city: str
    is_admin: bool

    class Config:
        from_attributes = True