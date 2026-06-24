from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel
from sqlalchemy.orm import Session
import models
from database import engine, get_db

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

class NoteRequest(BaseModel):
    title: str
    content: str

@app.get("/")
def home():
    return {"message": "Welcome to the Notes API!"}

@app.post("/notes")
def create_note(note: NoteRequest, db: Session = Depends(get_db)):
    new_note = models.Note(title=note.title, content=note.content)
    db.add(new_note)
    db.commit()
    db.refresh(new_note)
    return new_note

@app.get("/notes")
def get_notes(db: Session = Depends(get_db)):
    notes = db.query(models.Note).all()
    return {"notes" : notes}

@app.delete("/notes/{note_id}")
def delete_note(note_id: int, db: Session = Depends(get_db)):
    note = db.query(models.Note).filter(models.Note.id == note_id).first()
    if note is None:
        raise HTTPException(status_code=404, detail="Note not found")
    db.delete(note)
    db.commit()
    return {"deleted": note}