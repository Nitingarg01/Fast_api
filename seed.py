"""
Run this once to populate the DB with sample notes for testing.
  python seed.py
"""
from database import SessionLocal, engine
import models, schemas, crud

models.Base.metadata.create_all(bind=engine)

sample_notes = [
    {
        "title": "FastAPI Basics",
        "content": "FastAPI is a modern, fast web framework for building APIs with Python 3.7+ based on standard Python type hints.",
        "tags": ["python", "fastapi", "backend"]
    },
    {
        "title": "SQLAlchemy ORM Tips",
        "content": "Use lazy='joined' for relationships you always need. Use session.flush() when you need the ID before commit.",
        "tags": ["python", "sqlalchemy", "database"]
    },
    {
        "title": "Shopping List",
        "content": "Milk, eggs, bread, butter, apples, and coffee beans.",
        "tags": ["personal", "todo"]
    },
    {
        "title": "Meeting Notes - Q2 Planning",
        "content": "Discussed roadmap for Q2. Key priorities: API performance, new search feature, mobile app launch.",
        "tags": ["work", "meetings"]
    },
    {
        "title": "Python List Comprehensions",
        "content": "List comprehensions provide a concise way to create lists. Example: squares = [x**2 for x in range(10)]",
        "tags": ["python", "tips"]
    },
]

db = SessionLocal()
for data in sample_notes:
    note = schemas.NoteCreate(**data)
    crud.create_note(db, note)
    print(f"  ✅ Created: '{data['title']}'")

db.close()
print("\n🎉 Seed complete! Run: uvicorn main:app --reload")