from pydantic import BaseModel, EmailStr, constr, validator
from typing import Optional, List
from datetime import date, datetime
import re


class AuthorBase(BaseModel):
    name: str
    biography: Optional[str] = None
    birth_date: Optional[date] = None
    nationality: Optional[str] = None


class AuthorCreate(AuthorBase):
    pass


class Author(AuthorBase):
    id: int

    class Config:
        orm_mode = True


class BookBase(BaseModel):
    title: str
    genre: str
    page_count: int
    publication_year: int
    description: str


class BookCreate(BookBase):
    authors: List[AuthorCreate]  
    cover_image: Optional[str] = None


class Book(BookBase):
    id: int
    authors: List[Author]  
    cover_image: Optional[str] = None

    class Config:
        orm_mode = True


class BookUpdate(BaseModel):
    title: Optional[str] = None
    genre: Optional[str] = None
    page_count: Optional[int] = None
    publication_year: Optional[int] = None
    description: Optional[str] = None
    cover_image: Optional[str] = None
    authors: Optional[List[AuthorCreate]] = None  

    class Config:
        orm_mode = True




class UserBase(BaseModel):
    email: EmailStr
    full_name: Optional[str] = None


class UserCreate(UserBase):
    password: constr(min_length=8)
    role: str = "Member"  

    @validator('password')
    def password_strength(cls, v):
        if len(v) < 8:
            raise ValueError('Password must be at least 8 characters long')
        if not re.search(r'[A-Z]', v):
            raise ValueError('Password must contain at least one uppercase letter')
        if not re.search(r'[a-z]', v):
            raise ValueError('Password must contain at least one lowercase letter')
        if not re.search(r'[0-9]', v):
            raise ValueError('Password must contain at least one digit')
        if not re.search(r'[!@#$%^&*(),.?":{}|<>]', v):
            raise ValueError('Password must contain at least one special character')
        return v


class User(UserBase):
    id: int
    is_active: bool
    role: str

    class Config:
        orm_mode = True


# Schemas for Authentication

class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    email: Optional[str] = None
    role: Optional[str] = None
    id: Optional[int] = None  


class UserLogin(BaseModel):
    email: str
    password: str


# Schemas for Reviews

class ReviewBase(BaseModel):
    rating: int = ...  
    text: Optional[str] = None

    class Config:
        orm_mode = True


class ReviewCreate(ReviewBase):
    book_id: int  


class ReviewOut(ReviewBase):
    id: int
    user_id: int
    created_at: datetime

    class Config:
        orm_mode = True
