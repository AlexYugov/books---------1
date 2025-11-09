from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base

class Favorite(Base):
    __tablename__ = "favorites"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    book_id = Column(Integer, ForeignKey("books.id"))

    user = relationship("User", back_populates="favorites")
    book = relationship("Book", back_populates="favorites")