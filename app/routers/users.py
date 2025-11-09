from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from app.database import get_db  # Changed import
from app.utils.auth import get_current_user, get_password_hash  # Changed import
from app.models.user import User
from app.repositories.user import UserRepository
from app.repositories.book import BookRepository
from app.schemas.user import UserCreate, UserSchema, UserUpdate
from app.schemas.book import BookSchema

router = APIRouter()

@router.post("/register", response_model=UserSchema)
async def register_user(
    user: UserCreate,
    db: Session = Depends(get_db)
):
    user_repository = UserRepository(db)
    if user_repository.get_user_by_login(user.login):
        raise HTTPException(status_code=400, detail="Login already registered")
    if user_repository.get_user_by_email(user.email):
        raise HTTPException(status_code=400, detail="Email already registered")
    if len(user.password) < 8:
        raise HTTPException(status_code=400, detail="Password must be at least 8 characters")
    return user_repository.create_user(user)

@router.get("/users/me", response_model=UserSchema)
async def get_current_user_data(
    current_user: User = Depends(get_current_user)
):
    return current_user

@router.get("/users/{id}", response_model=UserSchema)
async def get_user(
    id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    user_repository = UserRepository(db)
    user = user_repository.get_user_by_id(id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

@router.get("/users/by-login/{login}", response_model=UserSchema)
async def get_user_by_login(
    login: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    user_repository = UserRepository(db)
    user = user_repository.get_user_by_login(login)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

@router.get("/users", response_model=List[UserSchema])
async def get_users(
    skip: int = 0,
    limit: int = 10,
    city: str = "",
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    if not current_user.is_admin:
        raise HTTPException(status_code=403, detail="Admin access required")
    user_repository = UserRepository(db)
    users = user_repository.get_users(skip, limit, city)
    return users

@router.put("/users/{id}", response_model=UserSchema)
async def update_user(
    id: int,
    user: UserUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    if id != current_user.id and not current_user.is_admin:
        raise HTTPException(status_code=403, detail="Not authorized")
    user_repository = UserRepository(db)
    db_user = user_repository.get_user_by_id(id)
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")
    if user.login and user_repository.get_user_by_login(user.login) and user.login != db_user.login:
        raise HTTPException(status_code=400, detail="Login already taken")
    if user.email and user_repository.get_user_by_email(user.email) and user.email != db_user.email:
        raise HTTPException(status_code=400, detail="Email already taken")
    updated_user = user_repository.update_user(id, user)
    return updated_user

@router.delete("/users/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(
    id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    if not current_user.is_admin:
        raise HTTPException(status_code=403, detail="Admin access required")
    user_repository = UserRepository(db)
    db_user = user_repository.get_user_by_id(id)
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")
    if db_user.id == current_user.id:
        raise HTTPException(status_code=400, detail="Cannot delete own account")
    user_repository.delete_user(id)
    return None

@router.get("/users/me/books", response_model=List[BookSchema])
async def get_user_books(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    book_repository = BookRepository(db)
    books = book_repository.get_user_books(current_user.id)
    return books