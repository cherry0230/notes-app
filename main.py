from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI()

notes = {}
counter = {"id": 1}

class Note(BaseModel):
    title: str
    content: str

@app.get("/")
def home():
    return {"message": "Notes API is running"}

@app.post("/notes")
def create_note(note: Note):
    note_id = counter["id"]
    notes[note_id] = {"id": note_id, "title": note.title, "content": note.content}
    counter["id"] += 1
    return notes[note_id]

@app.get("/notes")
def get_notes():
    return {"notes": list(notes.values())}

@app.delete("/notes/{note_id}")
def delete_note(note_id: int):
    if note_id not in notes:
        raise HTTPException(status_code=404, detail="Note not found")
    deleted = notes.pop(note_id)
    return {"deleted": deleted}