from sqlalchemy import Column, Integer, String, Boolean
from sqlalchemy.orm import relationship
from app.database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    login = Column(String, unique=True, index=True)
    email = Column(String, unique=True, index=True)
    city = Column(String, nullable=False)
    password_hash = Column(String)
    is_admin = Column(Boolean, default=False)

    books = relationship("Book", back_populates="owner")
    favorites = relationship("Favorite", back_populates="user")
    comments = relationship("Comment", back_populates="user")