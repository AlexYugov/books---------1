from sqlalchemy.orm import Session
from app.models.comment import Comment
from app.schemas.comment import CommentCreate

class CommentRepository:
    def __init__(self, session: Session):
        self.db = session

    def create_comment(self, comment: CommentCreate, user_id: int, book_id: int):
        db_comment = Comment(content=comment.content, user_id=user_id, book_id=book_id)
        self.db.add(db_comment)
        self.db.commit()
        self.db.refresh(db_comment)
        return db_comment

    def get_comments_by_book_id(self, book_id: int, skip: int = 0, limit: int = 10):
        return self.db.query(Comment).filter(Comment.book_id == book_id).offset(skip).limit(limit).all()

    def get_comment_by_id(self, comment_id: int):  # Added method
        return self.db.query(Comment).filter(Comment.id == comment_id).first()

    def update_comment(self, comment_id: int, content: str):
        db_comment = self.get_comment_by_id(comment_id)
        if db_comment:
            db_comment.content = content
            self.db.commit()
            self.db.refresh(db_comment)
        return db_comment

    def delete_comment(self, comment_id: int):
        db_comment = self.get_comment_by_id(comment_id)
        if db_comment:
            self.db.delete(db_comment)
            self.db.commit()
        return db_comment