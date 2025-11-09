from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from app.database import get_db  # Changed import
from app.utils.auth import get_current_user  # Changed import
from app.models.user import User
from app.repositories.favorite import FavoriteRepository
from app.repositories.book import BookRepository
from app.schemas.favorite import FavoriteCreate, FavoriteSchema

router = APIRouter()

@router.post("/favorites", response_model=FavoriteSchema)
async def add_favorite(
    favorite: FavoriteCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    book_repository = BookRepository(db)
    if not book_repository.get_book_by_id(favorite.book_id):
        raise HTTPException(status_code=404, detail="Book not found")
    favorite_repository = FavoriteRepository(db)
    if favorite_repository.is_favorited(current_user.id, favorite.book_id):
        raise HTTPException(status_code=400, detail="Book already in favorites")
    db_favorite = favorite_repository.add_favorite(favorite, current_user.id)
    return db_favorite

@router.get("/favorites", response_model=List[FavoriteSchema])
async def get_favorites(
    skip: int = 0,
    limit: int = 5,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    favorite_repository = FavoriteRepository(db)
    favorites = favorite_repository.get_favorites(current_user.id, skip, limit)
    return favorites

@router.get("/favorites/is_favorited")
async def is_favorited(
    book_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    book_repository = BookRepository(db)
    if not book_repository.get_book_by_id(book_id):
        raise HTTPException(status_code=404, detail="Book not found")
    favorite_repository = FavoriteRepository(db)
    return {"is_favorited": favorite_repository.is_favorited(current_user.id, book_id)}

@router.delete("/favorites/{book_id}", status_code=status.HTTP_204_NO_CONTENT)
async def remove_favorite(
    book_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    book_repository = BookRepository(db)
    if not book_repository.get_book_by_id(book_id):
        raise HTTPException(status_code=404, detail="Book not found")
    favorite_repository = FavoriteRepository(db)
    if not favorite_repository.is_favorited(current_user.id, book_id):
        raise HTTPException(status_code=404, detail="Book not in favorites")
    favorite_repository.delete_favorite(current_user.id, book_id)
    return None