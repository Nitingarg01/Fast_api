from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, DeclarativeBase

# ── MariaDB connection ─────────────────────────────────────────────────────
# Format: mysql+pymysql://<user>:<password>@<host>:<port>/<database>
# Change the values below to match your MariaDB setup
DB_USER     = "root"
DB_PASSWORD = "root123"
DB_HOST     = "localhost"
DB_PORT     = "3306"
DB_NAME     = "smart_notes"

DATABASE_URL = f"mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

engine = create_engine(
    DATABASE_URL,
    pool_pre_ping=True,   # auto-reconnect if connection drops
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

class Base(DeclarativeBase):
    pass