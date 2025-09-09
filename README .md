# Book Library Management API

## Overview

This project is a Book Library Management API built with **FastAPI**, extending a basic CRUD backend by adding user authentication, database migrations, and enhanced data relationships.  
It supports multi-author books, user reviews, secure JWT-based authentication with role-based access control, and Alembic-managed database versioning.  
The API enables users to register, login, manage books with multiple authors, submit reviews, and provides different permissions for **Admin** and **Member** roles.

---

## Features

- **User Registration** with secure password hashing and role assignment (Admin/Member).
- **JWT Authentication** with access token generation, expiration, and secure session management.
- **Multi-author Book Management** via many-to-many relationships.
- **Dedicated Author entity** with biographical details.
- **Book Review System** with ratings and text reviews linked to authenticated users.
- **Database migrations** with Alembic for version control and rollback support.
- **Role-Based Access Control** restricting access based on user roles.
- **Enhanced foreign key relationships** and cascading deletes for data integrity.

---

## Technical Stack

| Component      | Technology                    |
|:-------------- |:-----------------------------|
| **Language**   | Python 3.9+                   |
| **Framework**  | FastAPI                       |
| **Database**   | PostgreSQL 13+                |
| **ORM**        | SQLAlchemy                    |
| **Migration**  | Alembic                       |
| **Auth**       | JWT with role-based auth      |
| **Validation** | Pydantic                      |
| **Security**   | bcrypt password hashing       |

---

## Setup Instructions

### Prerequisites

- Python 3.9+
- PostgreSQL 13+
- Git

### Clone the Repository

git clone <your_repository_url>
cd Book_Library_Management_API
### Create and Activate Virtual Environment

python -m venv venv
source venv/bin/activate # On Linux/Mac
venv\Scripts\activate # On Windows
### Install Dependencies
pip install -r requirements.txt
### Configure Database

Ensure PostgreSQL is running locally.  
Create the database:

CREATE DATABASE book_library_db;
Update connection URL if needed in `alembic.ini`:

postgresql://postgres:Anirudh@localhost:5432/book_library_db
### Run Database Migrations

alembic upgrade head
This applies all Alembic migration scripts to create and update database schema.

---

## Running the Application

Launch the API server:

uvicorn main:app --reload
- The API will be accessible at: `http://127.0.0.1:8000`
- Test the health endpoint:

GET /ping[9]

---

## Authentication Flow

- **Registration**: `POST /users/register`  
  Send email, password (strong password enforced), full name, and optional role (defaults to Member)[9]
- **Login**: `POST /users/login`  
  Send username (email) and password; returns a JWT access token
- **Token Usage**:  
  Include `Authorization: Bearer <token>` header for authenticated requests
- **Role-Based Access**:  
  Admin users have elevated privileges (e.g., delete and update books); Members have restricted access

---

## API Endpoints Summary

### User

| Endpoint         | Method | Description               | Auth Required |
|------------------|--------|--------------------------|--------------|
| /users/register  | POST   | Register new user        | No           |
| /users/login     | POST   | User login, returns JWT  | No           |

---

### Books

| Endpoint         | Method  | Description                                 | Auth Required      |
|------------------|---------|---------------------------------------------|--------------------|
| /books/          | POST    | Create new book, multi-author support       | Yes               |
| /books/          | GET     | List books, optional filters                | Yes               |
| /books/{id}      | GET     | Get book details by ID                      | Yes               |
| /books/{id}      | DELETE  | Delete book                                 | Admin only        |
| /books/{id}      | PATCH   | Update book fields                          | Admin only        |

---

### Reviews

| Endpoint                | Method | Description                      | Auth Required |
|-------------------------|--------|----------------------------------|--------------|
| /reviews/               | POST   | Authenticated users submit reviews| Yes           |
| /reviews/book/{book_id} | GET    | Get all reviews for a book       | No            |

---

### Authors

Author data is managed internally via the book endpoints through multi-author support.  
Dedicated author management endpoints can be added as future work.

---

## Database Schema & Relationships

- **Books** and **Authors**: Many-to-many relationship via association table
- **Reviews**: Link users to books with ratings and optional text
- **Users**: Roles (Admin or Member) controlling access
- **Referential Integrity**: Enforced with cascade deletes on related entities

---

## Development Workflow

- Use Alembic for all schema changes:
  - Create migrations with:  
    `alembic revision --autogenerate -m "Message"`
  - Apply migrations with:  
    `alembic upgrade head`
- Commit code regularly with meaningful messages
- Follow Pydantic schemas for data validation
- Use provided utilities for password hashing and JWT token creation

---

## Testing

- Use provided Postman collection for book-related endpoints
- Authentication and review endpoints to be added for comprehensive testing
- Include Authorization header (from login) for protected endpoints

---
