# main.py
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.database import Base, engine
from app.routes import orders, refunds, error_logs, manual_reviews, scheduled_emails, leads, auth  # ← ADDED auth
from app.core.config import settings

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Create all database tables on startup
    Base.metadata.create_all(bind=engine)
    print("✅ Database tables created successfully.")
    print("📦 Tables: users, orders, refunds, error_logs, manual_reviews, scheduled_emails, leads")
    yield

app = FastAPI(
    title="BizLink B2B Workflow Automation",
    description="Backend API for BizLink platform - CSE 314 Group 3",
    version="1.0.0",
    lifespan=lifespan
)

# CORS Middleware (required when frontend is connected later)
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins_list,  # ← Use the parsed list
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Register routers
# main.py - CHANGE THIS LINE
app.include_router(auth.router, tags=["Authentication"])  # ← Remove prefix="/auth"
app.include_router(orders.router)
app.include_router(refunds.router)
app.include_router(error_logs.router)
app.include_router(manual_reviews.router)
app.include_router(scheduled_emails.router)
app.include_router(leads.router)

@app.get("/", operation_id="root_health_check")
def root():
    return {
        "message": "BizLink backend is running",
        "endpoints": {
            "auth": "/auth",
            "orders": "/orders",
            "refunds": "/refunds", 
            "error_logs": "/error-logs",
            "manual_reviews": "/manual-reviews",
            "scheduled_emails": "/scheduled-emails",
            "leads": "/leads",
            "docs": "/docs"
        }
    }