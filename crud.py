from sqlalchemy.orm import Session
from sqlalchemy import or_
from typing import List, Optional
import models, schemas


# ── Helpers ───────────────────────────────────────────────────────────────────

def get_or_create_tag(db: Session, name: str) -> models.Tag:
    """Fetch existing tag or create a new one."""
    tag = db.query(models.Tag).filter(models.Tag.name == name.lower().strip()).first()
    if not tag:
        tag = models.Tag(name=name.lower().strip())
        db.add(tag)
        db.flush()   # get the ID without committing
    return tag


def resolve_tags(db: Session, tag_names: List[str]) -> List[models.Tag]:
    return [get_or_create_tag(db, name) for name in tag_names if name.strip()]


# ── Notes CRUD ────────────────────────────────────────────────────────────────

def create_note(db: Session, note: schemas.NoteCreate) -> models.Note:
    tags = resolve_tags(db, note.tags)
    db_note = models.Note(title=note.title, content=note.content, tags=tags)
    db.add(db_note)
    db.commit()
    db.refresh(db_note)
    return db_note


def get_note(db: Session, note_id: int) -> Optional[models.Note]:
    return db.query(models.Note).filter(models.Note.id == note_id).first()


def get_notes(
    db: Session,
    skip: int = 0,
    limit: int = 10,
    search: Optional[str] = None,
    tag: Optional[str] = None,
) -> List[models.Note]:
    query = db.query(models.Note)

    # Keyword search in title OR content
    if search:
        pattern = f"%{search}%"
        query = query.filter(
            or_(
                models.Note.title.ilike(pattern),
                models.Note.content.ilike(pattern),
            )
        )

    # Filter by tag name
    if tag:
        query = query.join(models.Note.tags).filter(
            models.Tag.name == tag.lower().strip()
        )

    return query.order_by(models.Note.created_at.desc()).offset(skip).limit(limit).all()


def update_note(
    db: Session, note_id: int, note_data: schemas.NoteUpdate
) -> Optional[models.Note]:
    db_note = get_note(db, note_id)
    if not db_note:
        return None

    if note_data.title is not None:
        db_note.title = note_data.title
    if note_data.content is not None:
        db_note.content = note_data.content
    if note_data.tags is not None:
        db_note.tags = resolve_tags(db, note_data.tags)

    db.commit()
    db.refresh(db_note)
    return db_note


def delete_note(db: Session, note_id: int) -> bool:
    db_note = get_note(db, note_id)
    if not db_note:
        return False
    db.delete(db_note)
    db.commit()
    return True


# ── Tags ──────────────────────────────────────────────────────────────────────

def get_all_tags(db: Session) -> List[models.Tag]:
    return db.query(models.Tag).order_by(models.Tag.name).all()


def get_notes_by_tag(db: Session, tag_name: str) -> List[models.Note]:
    return (
        db.query(models.Note)
        .join(models.Note.tags)
        .filter(models.Tag.name == tag_name.lower().strip())
        .order_by(models.Note.created_at.desc())
        .all()
    )


# ── Search ────────────────────────────────────────────────────────────────────

def search_notes(db: Session, query: str) -> List[models.Note]:
    """
    Search notes by keyword in title and content.
    Results sorted: title matches first, then content matches.
    """
    pattern = f"%{query}%"
    title_matches = (
        db.query(models.Note)
        .filter(models.Note.title.ilike(pattern))
        .all()
    )
    content_matches = (
        db.query(models.Note)
        .filter(
            models.Note.content.ilike(pattern),
            ~models.Note.id.in_([n.id for n in title_matches])  # avoid duplicates
        )
        .all()
    )
    return title_matches + content_matches