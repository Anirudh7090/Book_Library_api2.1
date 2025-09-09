from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from app.models.models import Review
from app.schemas.schemas import ReviewCreate, ReviewOut, TokenData
from app.db.db import get_db

from app.dependencies.dependencies import get_current_user

router = APIRouter(
    prefix="/reviews",
    tags=["Reviews"],
)

@router.post("/", response_model=ReviewOut, status_code=status.HTTP_201_CREATED)
def create_review(
    review: ReviewCreate,
    db: Session = Depends(get_db),
    current_user: TokenData = Depends(get_current_user),
):
    print("Incoming review POST request")
    print(f"Review data: {review}")
    print(f"Current user: {current_user}")

    if not current_user.id:
        raise HTTPException(status_code=401, detail="User ID missing from token.")

    db_review = Review(
        book_id=review.book_id,
        user_id=current_user.id,  # Correctly set user_id to integer ID from token
        rating=review.rating,
        text=review.text,
    )
    db.add(db_review)
    db.commit()
    db.refresh(db_review)
    print(f"Review created with id: {db_review.id}")
    return db_review

@router.get("/book/{book_id}", response_model=List[ReviewOut])
def get_book_reviews(book_id: int, db: Session = Depends(get_db)):
    reviews = db.query(Review).filter(Review.book_id == book_id).all()
    print(f"Fetched {len(reviews)} reviews for book_id {book_id}")
    return reviews
