import traceback
print("STARTING FASTAPI MAIN")

from fastapi import FastAPI, Depends, HTTPException, UploadFile, File, Query, Form, Body, Path, status, Request
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from typing import List, Optional
import shutil
import os
import json

import app.utils as utils
from app.crud import crud
from app.schemas import schemas
from app.models import models
from app.db.db import SessionLocal, engine, Base

from app.api.routers.users import router as users_router
from app.api.routers import reviews
from app.dependencies.dependencies import get_current_user

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Book Library Management API")

@app.get("/ping")
def ping():
    print("Ping endpoint called")
    return {"message": "pong"}

# Include routers
app.include_router(users_router, prefix="/users", tags=["users"])
app.include_router(reviews.router)

# Static directory for file uploads
STATIC_DIR = "../static"
os.makedirs(STATIC_DIR, exist_ok=True)

# Database session dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Global exception handler
@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    print(f"Unhandled exception: {exc}")
    traceback.print_exc()
    return JSONResponse(
        status_code=500,
        content={"detail": "Internal Server Error"}
    )

# Admin role check dependency
def admin_required(current_user: schemas.TokenData = Depends(get_current_user)):
    if not hasattr(current_user, "role") or current_user.role.lower() != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Admin privileges required",
        )
    return current_user

# Request logging middleware
@app.middleware("http")
async def log_requests(request: Request, call_next):
    utils.log_info(f"Incoming request: {request.method} {request.url}")
    response = await call_next(request)
    utils.log_info(f"Completed request: {request.method} {request.url} with status {response.status_code}")
    return response

# Create book endpoint
@app.post("/books/", response_model=schemas.Book)
def create_book(
    book: str = Form(...),
    cover_image: Optional[UploadFile] = File(None),
    db: Session = Depends(get_db),
    current_user: schemas.TokenData = Depends(get_current_user),
):
    print("Create book endpoint called")
    print("Raw book data string:", book)

    try:
        book_data = json.loads(book)
        print("Parsed book data:", book_data)
        book_obj = schemas.BookCreate(**book_data)
    except Exception as e:
        print("Error parsing book data:", e)
        raise HTTPException(status_code=400, detail=f"Invalid book data: {str(e)}")

    try:
        if cover_image:
            file_location = f"{STATIC_DIR}/{cover_image.filename}"
            with open(file_location, "wb") as buffer:
                shutil.copyfileobj(cover_image.file, buffer)
            book_obj.cover_image = file_location

        created_book = crud.create_book(db, book_obj)
        utils.log_info(f"Created book '{created_book.title}' by authors {[author.name for author in created_book.authors]}")
        return created_book
    except Exception as e:
        print("Error creating book:", e)
        raise HTTPException(status_code=500, detail=f"Internal error creating book: {str(e)}")

# List books endpoint
@app.get("/books/", response_model=List[schemas.Book])
def list_books(
    skip: int = 0,
    limit: int = 10,
    search: Optional[str] = Query(None, description="Search by title or author"),
    genre: Optional[str] = Query(None),
    author: Optional[str] = Query(None),
    db: Session = Depends(get_db),
    current_user: schemas.TokenData = Depends(get_current_user),
):
    if search:
        return crud.search_books(db, search, skip, limit)

    query = db.query(models.Book)
    if genre:
        query = query.filter(models.Book.genre.ilike(f"%{genre}%"))
    if author:
        query = query.join(models.Book.authors).filter(models.Author.name.ilike(f"%{author}%"))
    books = query.offset(skip).limit(limit).all()
    return books

# Get single book endpoint
@app.get("/books/{book_id}", response_model=schemas.Book)
def get_book(
    book_id: int,
    db: Session = Depends(get_db),
    current_user: schemas.TokenData = Depends(get_current_user),
):
    book = crud.get_book(db, book_id)
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")
    return book

# Delete book endpoint
@app.delete("/books/{book_id}")
def delete_book(
    book_id: int,
    db: Session = Depends(get_db),
    current_user: schemas.TokenData = Depends(admin_required),
):
    book = crud.get_book(db, book_id)
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")

    if book.cover_image and os.path.isfile(book.cover_image):
        os.remove(book.cover_image)

    crud.delete_book(db, book_id)
    utils.log_info(f"Deleted book id {book_id}")
    return {"detail": "Book deleted successfully"}

# Update book endpoint
@app.patch("/books/{book_id}", response_model=schemas.Book)
def update_book(
    book_id: int = Path(..., description="ID of the book to update"),
    book_update: schemas.BookUpdate = Body(...),
    db: Session = Depends(get_db),
    current_user: schemas.TokenData = Depends(admin_required),
):
    existing_book = crud.get_book(db, book_id)
    if not existing_book:
        raise HTTPException(status_code=404, detail="Book not found")

    updated_book = crud.update_book(db, book_id, book_update)
    return updated_book
