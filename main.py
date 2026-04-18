from contextlib import asynccontextmanager
from fastapi import FastAPI
from app.database import Base, engine

# Lifespan: Run this code when the server starts up
@asynccontextmanager
async def lifespan(app: FastAPI):
    # Create database tables on startup
    Base.metadata.create_all(bind=engine)
    print("✅ Database tables created successfully.")
    yield

app = FastAPI(
    title="Bizlink B2B Workflow Automation",
    description="Backend API for Bizlink platform",
    version="1.0.0",
    lifespan=lifespan
)

@app.get("/")
def root():
    return {"message": "Bizlink backend is running"}