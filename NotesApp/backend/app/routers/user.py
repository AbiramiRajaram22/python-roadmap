from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from app.core.dependencies import get_db
from app.exceptions import DuplicateUserException, NoDataFoundException
from app.schemas.user import UserCreate, UserUpdate, UserResponse
from app.crud.user import (
    create_user, get_users, get_user_by_id, update_user, delete_user,
    get_user_by_email, get_user_by_username
)

router = APIRouter()

@router.post("", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def create_user_endpoint(user: UserCreate, db: Session = Depends(get_db)):
    # Check if user already exists
    db_user = get_user_by_email(db, email=user.email)
    if db_user:
        raise DuplicateUserException("Email already registered")
    
    db_user = get_user_by_username(db, username=user.username)
    if db_user:
        raise DuplicateUserException("Username already taken")
    
    return create_user(db=db, user=user)

@router.get("", response_model=List[UserResponse])
async def get_users_endpoint(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    users = get_users(db, skip=skip, limit=limit)
    if users:
        raise NoDataFoundException("No users found")
    return users

@router.get("/{user_id}", response_model=UserResponse)
async def get_user_endpoint(user_id: int, db: Session = Depends(get_db)):
    db_user = get_user_by_id(db, user_id=user_id)
    if db_user is None:
        raise NoDataFoundException("No user found")        
    return db_user

@router.put("/{user_id}", response_model=UserResponse)
async def update_user_endpoint(user_id: int, user_update: UserUpdate, db: Session = Depends(get_db)):
    # Check if user exists
    db_user = get_user_by_id(db, user_id=user_id)
    if db_user is None:
        raise NoDataFoundException("No user found")      
    
    # Check for conflicts
    if user_update.email is not None:
        existing_user = get_user_by_email(db, user_update.email)
        if existing_user and existing_user.id != user_id:
            raise DuplicateUserException("Email already registered")
    
    if user_update.username is not None:
        existing_user = get_user_by_username(db, user_update.username)
        if existing_user and existing_user.id != user_id:
            raise DuplicateUserException("Username already taken")
    
    updated_user = update_user(db=db, user_id=user_id, user_update=user_update)
    return updated_user

@router.delete("/{user_id}")
async def delete_user_endpoint(user_id: int, db: Session = Depends(get_db)):
    success = delete_user(db=db, user_id=user_id)
    if not success:
        raise NoDataFoundException("No user found")      
    return {"message": "User deleted successfully"}