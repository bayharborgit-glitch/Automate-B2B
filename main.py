from fastapi import FastAPI

app = FastAPI(
    title="BizLink B2B Workflow Automation",
    description="Backend API for BizLink platform",
    version="1.0.0"
)

@app.get("/")
def root():
    return {"message": "BizLink backend is running"}