from contextlib import asynccontextmanager
from fastapi import FastAPI
from app.database import Base, engine
from app.routes import orders  # <--- ADD THIS LINE

@asynccontextmanager
async def lifespan(app: FastAPI):
    Base.metadata.create_all(bind=engine)
    print("✅ Database tables created successfully.")
    yield

app = FastAPI(
    title="Bizlink B2B Workflow Automation",
    description="Backend API for Bizlink platform",
    version="1.0.0",
    lifespan=lifespan
)

# Include routers
app.include_router(orders.router)  # <--- ADD THIS LINE

@app.get("/")
def root():
    return {"message": "Bizlink backend is running"}