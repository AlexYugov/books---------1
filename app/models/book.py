from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base

class Book(Base):
    __tablename__ = "books"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    author = Column(String, index=True)
    genre = Column(String)
    year = Column(Integer)
    condition = Column(String)
    city = Column(String)
    cover_image = Column(String)
    contacts = Column(String, nullable=True)  # Добавлено поле для контактов
    status = Column(String, default="available")
    owner_id = Column(Integer, ForeignKey("users.id"))

    owner = relationship("User", back_populates="books")
    favorites = relationship("Favorite", back_populates="book")
    comments = relationship("Comment", back_populates="book")

    @property
    def owner_login(self):
        return self.owner.login if self.owner else None