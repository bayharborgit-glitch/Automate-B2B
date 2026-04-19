# app/database.py
# Minimal FastAPI + SQLAlchemy database setup - NO optional imports

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
import os

# 1. Database URL
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./bizlink.db")

# 2. SQLite-specific connect args
if DATABASE_URL.startswith("sqlite"):
    connect_args = {"check_same_thread": False}
else:
    connect_args = {}

# 3. Create engine
engine = create_engine(DATABASE_URL, connect_args=connect_args, echo=False)

# 4. Session factory
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# 5. Base for models
Base = declarative_base()

# 6. ✅ THE FUNCTION FASTAPI NEEDS - must be at module level, no nesting
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# 7. Debug print - confirms file is loaded
print(f"🔧 database.py loaded | get_db defined: {callable(get_db)}")