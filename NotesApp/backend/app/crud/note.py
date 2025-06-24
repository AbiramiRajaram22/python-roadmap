from sqlalchemy.orm import Session
from datetime import datetime
from app.models.note import Note
from app.schemas.note import NoteCreate, NoteUpdate

def get_notes_by_user(db: Session, user_id: int, skip: int = 0, limit: int = 100):
    return db.query(Note).filter(Note.owner_id == user_id).offset(skip).limit(limit).all()

def get_note_by_id(db: Session, note_id: int, user_id: int):
    return db.query(Note).filter(Note.id == note_id, Note.owner_id == user_id).first()

def create_note(db: Session, note: NoteCreate, user_id: int):
    db_note = Note(
        title=note.title,
        content=note.content,
        owner_id=user_id
    )
    db.add(db_note)
    db.commit()
    db.refresh(db_note)
    return db_note

def update_note(db: Session, note_id: int, note_update: NoteUpdate, user_id: int):
    db_note = db.query(Note).filter(Note.id == note_id, Note.owner_id == user_id).first()
    if not db_note:
        return None
    
    if note_update.title is not None:
        db_note.title = note_update.title
    if note_update.content is not None:
        db_note.content = note_update.content
    
    db_note.updated_at = datetime.utcnow()
    db.commit()
    db.refresh(db_note)
    return db_note

def delete_note(db: Session, note_id: int, user_id: int):
    db_note = db.query(Note).filter(Note.id == note_id, Note.owner_id == user_id).first()
    if db_note:
        db.delete(db_note)
        db.commit()
        return True
    return False