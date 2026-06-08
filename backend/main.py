from fastapi import FastAPI
from api.upload import router as upload_router
from api.ask import router as ask_router
from db.connection import engine, Base
from db import models

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="AI Knowledge System",
    description="RAG-based document Q&A",
    version="0.1.0"
)

app.include_router(upload_router, prefix="/api/v1", tags=["documents"])
app.include_router(ask_router, prefix="/api/v1", tags=["questions"])

@app.get("/")
def health_check():
    return {"status": "running", "message": "AI Knowledge System is live"}