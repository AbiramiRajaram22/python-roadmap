# FastAPI CRUD API with PostgreSQL

This project is a simple CRUD API built with **FastAPI**, connected to a **PostgreSQL** database.  
It includes endpoints for managing **Users** and **Notes**, with authentication and validation.

## 🚀 Features

- User registration and authentication (JWT-based)
- CRUD operations for Users and Notes
- PostgreSQL database integration via SQLAlchemy
- Secure password hashing
- Token-based authorization
- Input validation

## 📦 Packages Used

The following Python packages are used in this project:

- [`sqlalchemy`](https://pypi.org/project/SQLAlchemy/) – ORM for database operations  
- [`passlib[bcrypt]`](https://passlib.readthedocs.io/en/stable/) – For secure password hashing  
- [`python-jose[cryptography]`](https://python-jose.readthedocs.io/en/latest/) – For JWT token creation and validation  
- [`python-multipart`](https://pypi.org/project/python-multipart/) – For parsing `multipart/form-data`  
- [`psycopg2-binary`](https://pypi.org/project/psycopg2-binary/) – PostgreSQL database adapter  
- [`email-validator`](https://pypi.org/project/email-validator/) – For validating email addresses

## 🛠️ Endpoints

### 🔐 User Endpoints

- `POST /login` – Authenticate a user and return a token
- `POST /users/` – Register new user with hashed password
- `GET /users/` – List all users
- `GET /users/{id}` – Get a specific user by ID
- `PUT /users/{id}` – Update a user by ID
- `DELETE /users/{id}` – Delete a user by ID

### 📝 Note Endpoints

- `POST /notes/` – Create a new note
- `GET /notes/` – List all notes for the authenticated user
- `GET /notes/{id}` – Get a specific note by ID
- `PUT /notes/{id}` – Update a note by ID
- `DELETE /notes/{id}` – Delete a note by ID

## 🗃️ Database

- **PostgreSQL** is used as the database.
- Tables are defined using **SQLAlchemy ORM**.

## ▶️ Getting Started

1. Create a virtual environment  
   `python -m venv venv && source venv/bin/activate` (Linux/macOS)  
   `python -m venv venv && venv\Scripts\activate` (Windows)

2. Install dependencies  
   ```bash
   pip install -r requirements.txt

3. Run the server
   ```bash
   uvicorn main:app --reload
   ```
