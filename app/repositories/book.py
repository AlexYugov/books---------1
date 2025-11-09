from sqlalchemy.orm import Session
from app.models.book import Book
from app.models.user import User
from app.schemas.book import BookCreate

class BookRepository:
    def __init__(self, db: Session):
        self.db = db

    def create_book(self, book: BookCreate, owner_id: int):
        db_book = Book(**book.dict(), owner_id=owner_id, status="available")
        self.db.add(db_book)
        self.db.commit()
        self.db.refresh(db_book)
        return db_book

    def get_books(self, skip: int = 0, limit: int = 10, title: str = None, genre: str = None, city: str = None):
        query = self.db.query(Book).filter(Book.status == "available")
        if title:
            query = query.filter(Book.title.ilike(f"%{title}%"))
        if genre:
            query = query.filter(Book.genre == genre)
        if city:
            query = query.filter(Book.city.ilike(f"%{city}%"))
        return query.offset(skip).limit(limit).all()

    def get_book_by_id(self, book_id: int):
        return self.db.query(Book).filter(Book.id == book_id).first()

    def update_book(self, book_id: int, book_update: BookCreate):
        db_book = self.db.query(Book).filter(Book.id == book_id).first()
        if db_book:
            for key, value in book_update.dict().items():
                setattr(db_book, key, value)
            self.db.commit()
            self.db.refresh(db_book)
        return db_book

    def delete_book(self, book_id: int):
        db_book = self.db.query(Book).filter(Book.id == book_id).first()
        if db_book:
            self.db.delete(db_book)
            self.db.commit()
        return db_book

    def get_user_books(self, user_id: int):
        return self.db.query(Book).filter(Book.owner_id == user_id, Book.status == "available").all()
    
    def get_owner_login(self, book_id: int):
        return self.db.query(User.login).join(Book.owner).filter(Book.id == book_id).scalar()