# 📝 Smart Notes API

A production-grade REST API built with **FastAPI** + **SQLAlchemy** (SQLite) featuring full CRUD, keyword search, tag filtering, and pagination.

---

## 🚀 Quick Start

```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. (Optional) Seed sample data
python seed.py

# 3. Run the server
uvicorn main:app --reload
```

Open **http://127.0.0.1:8000/docs** for the interactive Swagger UI.

---

## 📁 Project Structure

```
smart_notes_api/
├── main.py          # FastAPI app & route definitions
├── database.py      # SQLAlchemy engine + session
├── models.py        # ORM models (Note, Tag, note_tags)
├── schemas.py       # Pydantic request/response schemas
├── crud.py          # All database operations
├── seed.py          # Sample data loader
└── requirements.txt
```

---

## 🔌 API Endpoints

### Notes
| Method | Endpoint         | Description                          |
|--------|-----------------|--------------------------------------|
| POST   | `/notes`         | Create a note (with tags)            |
| GET    | `/notes`         | List notes (search + tag + pagination)|
| GET    | `/notes/{id}`    | Get a single note                    |
| PUT    | `/notes/{id}`    | Update title, content, or tags       |
| DELETE | `/notes/{id}`    | Delete a note                        |

### Tags
| Method | Endpoint                 | Description                   |
|--------|--------------------------|-------------------------------|
| GET    | `/tags`                  | List all tags                 |
| GET    | `/tags/{tag_name}/notes` | All notes with this tag       |

### Search
| Method | Endpoint    | Description                            |
|--------|-------------|----------------------------------------|
| GET    | `/search?q=` | Full-text search (title + content)    |

---

## 💡 Example Requests

### Create a Note
```bash
curl -X POST http://localhost:8000/notes \
  -H "Content-Type: application/json" \
  -d '{
    "title": "FastAPI is great",
    "content": "Building APIs with FastAPI is really fast and fun.",
    "tags": ["python", "fastapi"]
  }'
```

### Search Notes
```bash
curl "http://localhost:8000/search?q=fastapi"
```

### Filter by Tag
```bash
curl "http://localhost:8000/notes?tag=python"
```

### Search + Pagination
```bash
curl "http://localhost:8000/notes?search=python&skip=0&limit=5"
```

---

## 🗄️ Database

Uses **SQLite** by default (`smart_notes.db` auto-created on first run).

To switch to **PostgreSQL**, update `DATABASE_URL` in `database.py`:
```python
DATABASE_URL = "postgresql://user:password@localhost/smart_notes"
```
Then remove the `connect_args` from `create_engine`.

---

## 🧠 Key Design Decisions

- **Many-to-many tags** via `note_tags` association table
- **Auto tag creation** — tags are created on-the-fly when a note is saved
- **Search ranking** — title matches returned before content matches
- **Case-insensitive** tag lookup and search
- **Cascade deletes** — deleting a note cleans up its tag associations