from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from app.database import get_db
from app.utils.auth import get_current_user
from app.models.user import User
from app.repositories.book import BookRepository
from app.schemas.book import BookCreate, BookSchema, BookUpdate

router = APIRouter()

@router.post("/books", response_model=BookSchema)
async def create_book(
    book: BookCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    if book.year < 0:
        raise HTTPException(status_code=400, detail="Year cannot be negative")
    book_repository = BookRepository(db)
    db_book = book_repository.create_book(book, current_user.id)
    return db_book

@router.get("/books", response_model=List[BookSchema])
async def get_books(
    skip: int = 0,
    limit: int = 5,
    title: str = "",
    genre: str = None,
    city: str = "",
    db: Session = Depends(get_db)
):
    book_repository = BookRepository(db)
    books = book_repository.get_books(
        skip=skip,
        limit=limit,
        title=title,
        genre=genre,
        city=city
    )
    return books

@router.get("/books/{id}", response_model=BookSchema)
async def get_book(
    id: int,
    db: Session = Depends(get_db)
):
    book_repository = BookRepository(db)
    book = book_repository.get_book_by_id(id)
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")
    return book

@router.put("/books/{id}", response_model=BookSchema)
async def update_book(
    id: int,
    book: BookUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    book_repository = BookRepository(db)
    db_book = book_repository.get_book_by_id(id)
    if not db_book:
        raise HTTPException(status_code=404, detail="Book not found")
    if db_book.owner_id != current_user.id and not current_user.is_admin:
        raise HTTPException(status_code=403, detail="Not authorized")
    if book.year and book.year < 0:
        raise HTTPException(status_code=400, detail="Year cannot be negative")
    updated_book = book_repository.update_book(id, book)
    return updated_book

@router.delete("/books/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_book(
    id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    book_repository = BookRepository(db)
    db_book = book_repository.get_book_by_id(id)
    if not db_book:
        raise HTTPException(status_code=404, detail="Book not found")
    if db_book.owner_id != current_user.id and not current_user.is_admin:
        raise HTTPException(status_code=403, detail="Not authorized")
    book_repository.delete_book(id)
    return None