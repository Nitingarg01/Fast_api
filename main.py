from fastapi import FastAPI, HTTPException, Depends, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from database import SessionLocal, engine
import models, schemas, crud

models.Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="📝 Smart Notes API",
    description="A smart note-taking API with full CRUD, keyword search, and tag filtering.",
    version="1.0.0"
)

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# ──────────────────────────────────────────
# NOTES ENDPOINTS
# ──────────────────────────────────────────

@app.post("/notes", response_model=schemas.NoteOut, status_code=201, tags=["Notes"])
def create_note(note: schemas.NoteCreate, db: Session = Depends(get_db)):
    """Create a new note with optional tags."""
    return crud.create_note(db, note)


@app.get("/notes", response_model=List[schemas.NoteOut], tags=["Notes"])
def list_notes(
    skip: int = Query(0, ge=0, description="Number of records to skip"),
    limit: int = Query(10, ge=1, le=100, description="Max records to return"),
    search: Optional[str] = Query(None, description="Keyword search in title/content"),
    tag: Optional[str] = Query(None, description="Filter notes by tag name"),
    db: Session = Depends(get_db)
):
    """
    List all notes with optional:
    - **search**: keyword search in title & content
    - **tag**: filter by tag name
    - **skip/limit**: pagination
    """
    return crud.get_notes(db, skip=skip, limit=limit, search=search, tag=tag)


@app.get("/notes/{note_id}", response_model=schemas.NoteOut, tags=["Notes"])
def get_note(note_id: int, db: Session = Depends(get_db)):
    """Get a single note by ID."""
    note = crud.get_note(db, note_id)
    if not note:
        raise HTTPException(status_code=404, detail=f"Note {note_id} not found")
    return note


@app.put("/notes/{note_id}", response_model=schemas.NoteOut, tags=["Notes"])
def update_note(note_id: int, note_data: schemas.NoteUpdate, db: Session = Depends(get_db)):
    """Update title, content, or tags of a note."""
    note = crud.update_note(db, note_id, note_data)
    if not note:
        raise HTTPException(status_code=404, detail=f"Note {note_id} not found")
    return note


@app.delete("/notes/{note_id}", tags=["Notes"])
def delete_note(note_id: int, db: Session = Depends(get_db)):
    """Delete a note by ID."""
    success = crud.delete_note(db, note_id)
    if not success:
        raise HTTPException(status_code=404, detail=f"Note {note_id} not found")
    return {"message": f"Note {note_id} deleted successfully"}


# ──────────────────────────────────────────
# TAGS ENDPOINTS
# ──────────────────────────────────────────

@app.get("/tags", response_model=List[schemas.TagOut], tags=["Tags"])
def list_tags(db: Session = Depends(get_db)):
    """List all available tags."""
    return crud.get_all_tags(db)


@app.get("/tags/{tag_name}/notes", response_model=List[schemas.NoteOut], tags=["Tags"])
def notes_by_tag(tag_name: str, db: Session = Depends(get_db)):
    """Get all notes that have a specific tag."""
    return crud.get_notes_by_tag(db, tag_name)


# ──────────────────────────────────────────
# SEARCH ENDPOINT
# ──────────────────────────────────────────

@app.get("/search", response_model=List[schemas.NoteOut], tags=["Search"])
def search_notes(
    q: str = Query(..., min_length=1, description="Search query"),
    db: Session = Depends(get_db)
):
    """
    Full keyword search across note title and content.
    Returns ranked results (most relevant first).
    """
    return crud.search_notes(db, q)


@app.get("/", tags=["Health"])
def root():
    return {
        "message": "📝 Smart Notes API is running!",
        "docs": "/docs",
        "redoc": "/redoc"
    }