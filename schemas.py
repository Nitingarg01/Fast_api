from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime


# ── Tag Schemas ──────────────────────────────
class TagBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=100, example="python")

class TagOut(TagBase):
    id: int

    class Config:
        from_attributes = True


# ── Note Schemas ─────────────────────────────
class NoteBase(BaseModel):
    title:   str  = Field(..., min_length=1, max_length=255, example="My First Note")
    content: str  = Field(..., min_length=1, example="This is the note content.")

class NoteCreate(NoteBase):
    tags: List[str] = Field(default=[], example=["python", "fastapi"])

class NoteUpdate(BaseModel):
    title:   Optional[str]       = Field(None, min_length=1, max_length=255)
    content: Optional[str]       = Field(None, min_length=1)
    tags:    Optional[List[str]] = None

class NoteOut(NoteBase):
    id:         int
    tags:       List[TagOut] = []
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True