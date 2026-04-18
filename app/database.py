from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Use SQLite for development (as requested in the initial plan)
# Switch to PostgreSQL for production later
SQLALCHEMY_DATABASE_URL = "sqlite:///./bizlink.db"

# Create the Engine
engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False}  # Required for SQLite only
)

# Create the Session Factory
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Create the Base Class (Our models will inherit from this)
Base = declarative_base()