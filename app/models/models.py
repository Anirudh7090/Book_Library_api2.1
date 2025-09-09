from sqlalchemy import (
    Table, Column, Integer, String, Boolean, ForeignKey, Date, Text, DateTime
)
from sqlalchemy.orm import relationship
import sqlalchemy as sa
from app.db.db import Base

# Association table for many-to-many relation between books and authors
book_author_table = Table(
    "book_author",
    Base.metadata,
    Column("book_id", Integer, ForeignKey("books.id", ondelete="CASCADE"), primary_key=True),
    Column("author_id", Integer, ForeignKey("authors.id", ondelete="CASCADE"), primary_key=True),
)

class Author(Base):
    __tablename__ = "authors"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    biography = Column(Text, nullable=True)
    birth_date = Column(Date, nullable=True)
    nationality = Column(String, nullable=True)

    books = relationship(
        "Book",
        secondary=book_author_table,
        back_populates="authors"
    )

class Book(Base):
    __tablename__ = "books"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True, nullable=False)
    genre = Column(String, index=True, nullable=False)
    page_count = Column(Integer, nullable=False)
    publication_year = Column(Integer, nullable=False)
    description = Column(Text, nullable=False)
    cover_image = Column(String, nullable=True)

    authors = relationship(
        "Author",
        secondary=book_author_table,
        back_populates="books"
    )
    reviews = relationship("Review", back_populates="book", cascade="all, delete-orphan")

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    full_name = Column(String, nullable=True)
    is_active = Column(Boolean, default=True)
    role = Column(String, default="member")

    reviews = relationship("Review", back_populates="user", cascade="all, delete-orphan")

class Review(Base):
    __tablename__ = "reviews"

    id = Column(Integer, primary_key=True, index=True)
    book_id = Column(Integer, ForeignKey("books.id", ondelete="CASCADE"))
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"))
    rating = Column(Integer, nullable=False)
    text = Column(Text, nullable=True)
    created_at = Column(DateTime, server_default=sa.func.now())

    book = relationship("Book", back_populates="reviews")
    user = relationship("User", back_populates="reviews")
