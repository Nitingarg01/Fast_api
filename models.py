from sqlalchemy import Column, Integer, String, Text, DateTime, Table, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from database import Base

# ── Association table (many-to-many: notes ↔ tags) ──
note_tags = Table(
    "note_tags",
    Base.metadata,
    Column("note_id", Integer, ForeignKey("notes.id", ondelete="CASCADE"), primary_key=True),
    Column("tag_id",  Integer, ForeignKey("tags.id",  ondelete="CASCADE"), primary_key=True),
)


class Note(Base):
    __tablename__ = "notes"

    id         = Column(Integer, primary_key=True, index=True)
    title      = Column(String(255), nullable=False, index=True)
    content    = Column(Text, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    tags = relationship("Tag", secondary=note_tags, back_populates="notes", lazy="joined")


class Tag(Base):
    __tablename__ = "tags"

    id   = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), unique=True, nullable=False, index=True)

    notes = relationship("Note", secondary=note_tags, back_populates="tags")