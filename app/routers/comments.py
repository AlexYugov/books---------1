from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from app.database import get_db  # Changed import
from app.utils.auth import get_current_user  # Changed import
from app.models.user import User
from app.repositories.comment import CommentRepository
from app.repositories.book import BookRepository
from app.schemas.comment import CommentCreate, CommentSchema, CommentUpdate

comments_router = APIRouter()

@comments_router.post("/books/{book_id}/comments", response_model=CommentSchema)
async def create_comment(
    book_id: int,
    comment: CommentCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    book_repository = BookRepository(db)
    if not book_repository.get_book_by_id(book_id):
        raise HTTPException(status_code=404, detail="Book not found")
    comment_repository = CommentRepository(db)
    db_comment = comment_repository.create_comment(comment, current_user.id, book_id)
    return db_comment

@comments_router.get("/books/{book_id}/comments", response_model=List[CommentSchema])
async def get_comments(
    book_id: int,
    skip: int = 0,
    limit: int = 10,
    db: Session = Depends(get_db)
):
    book_repository = BookRepository(db)
    if not book_repository.get_book_by_id(book_id):
        raise HTTPException(status_code=404, detail="Book not found")
    comment_repository = CommentRepository(db)
    comments = comment_repository.get_comments_by_book_id(book_id, skip, limit)
    return comments

@comments_router.put("/comments/{comment_id}", response_model=CommentSchema)
async def update_comment(
    comment_id: int,
    comment: CommentUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    comment_repository = CommentRepository(db)
    db_comment = comment_repository.get_comment_by_id(comment_id)  # Fixed: Added missing method
    if not db_comment:
        raise HTTPException(status_code=404, detail="Comment not found")
    if db_comment.user_id != current_user.id and not current_user.is_admin:
        raise HTTPException(status_code=403, detail="Not authorized")
    updated_comment = comment_repository.update_comment(comment_id, comment.content)
    return updated_comment

@comments_router.delete("/comments/{comment_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_comment(
    comment_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    comment_repository = CommentRepository(db)
    db_comment = comment_repository.get_comment_by_id(comment_id)  # Fixed: Added missing method
    if not db_comment:
        raise HTTPException(status_code=404, detail="Comment not found")
    if db_comment.user_id != current_user.id and not current_user.is_admin:
        raise HTTPException(status_code=403, detail="Not authorized")
    comment_repository.delete_comment(comment_id)
    return None