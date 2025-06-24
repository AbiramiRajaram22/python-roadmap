from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from app.core.dependencies import get_db, get_current_user
from app.exceptions import NoDataFoundException
from app.schemas.note import NoteCreate, NoteUpdate, NoteResponse
from app.models.user import User
from app.crud.note import (
    create_note, get_notes_by_user, get_note_by_id, update_note, delete_note
)

router = APIRouter()

@router.post("", response_model=NoteResponse, status_code=status.HTTP_201_CREATED)
async def create_note_endpoint(
    note: NoteCreate,
    current_user: User = Depends(get_current_user), 
    db: Session = Depends(get_db)
):
    return create_note(db=db, note=note, user_id=current_user.id)

@router.get("", response_model=List[NoteResponse])
async def get_notes_endpoint(
    skip: int = 0, 
    limit: int = 100, 
    current_user: User = Depends(get_current_user), 
    db: Session = Depends(get_db)
):
    notes = get_notes_by_user(db, user_id=current_user.id, skip=skip, limit=limit)
    if notes:
        raise NoDataFoundException("Note not found")
    return notes


@router.get("/{note_id}", response_model=NoteResponse)
async def get_note_endpoint(
    note_id: int, 
    current_user: User = Depends(get_current_user), 
    db: Session = Depends(get_db)
):
    note = get_note_by_id(db, note_id=note_id, user_id=current_user.id)
    if note is None:
        raise NoDataFoundException("Note not found")
    return note

@router.put("/{note_id}", response_model=NoteResponse)
async def update_note_endpoint(
    note_id: int, 
    note_update: NoteUpdate, 
    current_user: User = Depends(get_current_user), 
    db: Session = Depends(get_db)
):
    updated_note = update_note(db=db, note_id=note_id, note_update=note_update, user_id=current_user.id)
    if updated_note is None:
        raise NoDataFoundException("Note not found")
    return updated_note

@router.delete("/{note_id}")
async def delete_note_endpoint(
    note_id: int, 
    current_user: User = Depends(get_current_user), 
    db: Session = Depends(get_db)
):
    success = delete_note(db=db, note_id=note_id, user_id=current_user.id)
    if not success:
        raise NoDataFoundException("Note not found")
    return {"message": "Note deleted successfully"}