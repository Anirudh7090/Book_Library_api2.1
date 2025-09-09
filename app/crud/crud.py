from sqlalchemy.orm import Session
from typing import List, Optional
from app.models.models import Book, Author
from app.schemas.schemas import BookCreate, BookUpdate, AuthorCreate


# CRUD for Author

def get_author_by_id(db: Session, author_id: int) -> Optional[Author]:
    return db.query(Author).filter(Author.id == author_id).first()

def get_author_by_name(db: Session, name: str) -> Optional[Author]:
    return db.query(Author).filter(Author.name == name).first()

def create_author(db: Session, author_create: AuthorCreate) -> Author:
    db_author = Author(
        name=author_create.name,
        biography=author_create.biography,
        birth_date=author_create.birth_date,
        nationality=author_create.nationality,
    )
    db.add(db_author)
    db.commit()
    db.refresh(db_author)
    return db_author

def list_authors(db: Session, skip: int = 0, limit: int = 10) -> List[Author]:
    return db.query(Author).offset(skip).limit(limit).all()


# CRUD for Book with multi-author support

def create_book(db: Session, book_create: BookCreate) -> Book:
    authors = []
    for author_in in book_create.authors:
        db_author = get_author_by_name(db, author_in.name)
        if not db_author:
            db_author = create_author(db, author_in)
        authors.append(db_author)

    db_book = Book(
        title=book_create.title,
        genre=book_create.genre,
        page_count=book_create.page_count,
        publication_year=book_create.publication_year,
        description=book_create.description,
        cover_image=book_create.cover_image,
        authors=authors,
    )
    db.add(db_book)
    db.commit()
    db.refresh(db_book)
    return db_book


def get_books(db: Session, skip: int = 0, limit: int = 10) -> List[Book]:
    return db.query(Book).offset(skip).limit(limit).all()


def get_book(db: Session, book_id: int) -> Optional[Book]:
    return db.query(Book).filter(Book.id == book_id).first()


def delete_book(db: Session, book_id: int) -> Optional[Book]:
    book = db.query(Book).filter(Book.id == book_id).first()
    if not book:
        return None
    db.delete(book)
    db.commit()
    return book


def search_books(db: Session, query: str, skip: int = 0, limit: int = 10) -> List[Book]:
    q = f"%{query.lower()}%"
    # Note: update to handle authors once relationship is in place
    return db.query(Book).filter(
        (Book.title.ilike(q))  # Adjust author filter after relationships
    ).offset(skip).limit(limit).all()


def update_book(db: Session, book_id: int, book_update: BookUpdate) -> Optional[Book]:
    book = db.query(Book).filter(Book.id == book_id).first()
    if not book:
        return None

    update_data = book_update.dict(exclude_unset=True)

    if "authors" in update_data:
        authors = []
        for author_in in update_data["authors"]:
            db_author = get_author_by_name(db, author_in.name)
            if not db_author:
                db_author = create_author(db, author_in)
            authors.append(db_author)
        book.authors = authors
        del update_data["authors"]

    for key, value in update_data.items():
        setattr(book, key, value)

    db.commit()
    db.refresh(book)
    return book
