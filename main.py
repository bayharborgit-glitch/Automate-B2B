from contextlib import asynccontextmanager
from fastapi import FastAPI
from app.database import Base, engine
from app.models import lead, order, refund, manual_review  # ← Triggers all model imports

from app.routes import orders, error_logs, manual_reviews 
from app.routes import refunds  # ← ADD error_logs, manual_reviews
from app.routes import leads

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
app.include_router(orders.router)
app.include_router(error_logs.router)      # ← ADD THIS
app.include_router(manual_reviews.router)  # ← ADD THIS
app.include_router(refunds.router) 
app.include_router(leads.router)

@app.get("/")
def read_root():
    return {"message": "BizLink API is running"}
